from peewee import *
from api.models import db, TrackerData, TrackerDevices, ApiKeys
import api.calculations
import json
import datetime
import hashlib

# Exception that will respond with a bad request HTTP error message to client
class BadRequestError(Exception):
    pass

class Database:
    def __init__(self, host, port):
        # Specify the database startup params
        db.init(host=host, port=port, database="iceland", user="USER", password="PASSWORD")
        # Open a database connection
        db.connect()

    # Performs a generic select query on the database
    def select_data(self, data_format, requested_field_names, filter_func, filter_args):
        # If no data format specific, use default
        if data_format == None:
            data_format = "json"

        # Verify that data output format is supported
        data_formats_supported = ["json", "csv"]
        if data_format not in data_formats_supported:
            raise BadRequestError("The requested data_format is not supported.")

        # All possible calculated field names, mapped to a list of the real fields each calculation depends on
        possible_calculated_field_names = {
            "displacement": ["longitude", "latitude", "timestamp"],
            "velocity": ["longitude", "latitude", "timestamp"]
        }

        # If no fields specified, select all fields in the query
        if requested_field_names == []:
            requested_field_names = list(TrackerData.get_column_map().keys()) + list(possible_calculated_field_names.keys())

        # Prepare any calculated field names (ie. velocity is calculated from lat, long and time)
        calculated_field_names = []
        dependency_field_names = []
        for field_name in possible_calculated_field_names:
            if field_name in requested_field_names:
                calculated_field_names.append(field_name)

                # Make sure any required (aka. dependent) fields for the calculation are also fetched
                for depedency_field in possible_calculated_field_names[field_name]:
                    if not depedency_field in requested_field_names:
                        dependency_field_names.append(depedency_field)

        # Remove from the list of fields directly selected from the DB
        for field_name in calculated_field_names:
            requested_field_names.remove(field_name)


        # Obtain a list of the requested data model field classes
        requested_fields = self.field_names_to_fields(requested_field_names+dependency_field_names)

        # Select all records that adhere to the filtering function
        # (Only return data from the requested fields)
        query = filter_func(requested_fields, *filter_args)
        records = query.dicts()

        # Converts the peeWee.ModelSelect class to a standard Python array
        # because ModelSelect is not JSON serializable
        records_array = [r for r in records]

        if len(records_array) > 0:
            # Fill in calculated fields for this data
            remove_first_record = False

            if "displacement" in calculated_field_names:
                # Prepare vectors of calculations to perform
                lat_longs_before = []
                lat_longs_after = []
                for i in range(len(records_array)):
                    lat_longs_before.append((records_array[0]["latitude"], records_array[0]["longitude"]))
                    lat_longs_after.append((records_array[i]["latitude"], records_array[i]["longitude"]))

                # Calculate velocities all at once (vectorized for speed)
                calculated_displacements = api.calculations.displacement_m_vector(lat_longs_before, lat_longs_after)
                
                # Add calculated field values to output
                for i in range(0, len(records_array)):
                    records_array[i]["displacement"] = calculated_displacements[i]

            if "velocity" in calculated_field_names:
                if len(records_array) == 1:
                    raise BadRequestError("Not possible to calculate velocity from one record.")

                # Prepare vectors of calculations to perform
                lat_longs_before = []
                lat_longs_after = []
                times_before = []
                times_after = []
                for i in range(1, len(records_array)):
                    lat_longs_before.append((records_array[i-1]["latitude"], records_array[i-1]["longitude"]))
                    lat_longs_after.append((records_array[i]["latitude"], records_array[i]["longitude"]))
                    times_before.append(records_array[i-1]["timestamp"])
                    times_after.append(records_array[i]["timestamp"])

                # Calculate velocities all at once (vectorized for speed)
                calculated_velocities = api.calculations.velocity_a_s_vector(lat_longs_before, lat_longs_after, times_before, times_after)
                
                # Add calculated field values to output
                for i in range(1, len(records_array)):
                    records_array[i]["velocity"] = calculated_velocities[i-1]

                remove_first_record = True
        
            # Toggled if a calculated field is requested
            # Causes the first record to be removed from the response as it is invalid
            # ie. there is no "first" velocity - we need at least 2 positions to calculate the velocity
            if remove_first_record:
                records_array.pop(0)

            # Remove fields from the response that were a calculation dependecncy, but not originally requested
            for field in dependency_field_names:
                if field not in requested_field_names:
                    # Remove all occurences of that field in every record 
                    records_array = [{k:v for (k,v) in r.items() if k != field} for r in records_array]

        # Log message for response
        print(f"Responded with {len(records_array)} records")
        
        # Format the response body
        if data_format == "json":
            # Convert these formatted records into JSON
            return json.dumps(records_array, indent=2, default=str)
        elif data_format == "csv":
            # Convert these formatted records into CSV
            csv_string = ""

            # Append field names as first line
            csv_string += ",".join(requested_field_names+calculated_field_names) + "\r\n"
            # Append CSV representations of records
            for r in records_array:
                csv_string += ",".join([str(r[v]) for v in r]) + "\r\n"

            return csv_string

    # Selects records from the database and formats them for the API response
    def retrieve_records(self, data_format, requested_field_names, rover_id, timestamp_start, timestamp_end):
        rover_id_parsed = self.validate_rover_id(rover_id)

        # Verify that the timestamps are valid
        # Don't check if they are blank (an unbounded query on time start/end)
        if timestamp_start:
            self.validate_timestamp(timestamp_start, "timestamp_start")
        else:
            # If no start provided, use earliest MySQL datetime
            timestamp_start = "1000-01-01T00:00:00"

        if timestamp_end:
            self.validate_timestamp(timestamp_end, "timestamp_end")
        else:
            # If no end provided, use latest MySQL datetime
            timestamp_end = "9999-12-31T23:59:59"

        if timestamp_start and timestamp_end:
            if timestamp_start > timestamp_end:
                raise BadRequestError("The timestamp_start is at a later date than the timestamp_end.")

        return self.select_data(
            data_format=data_format,
            requested_field_names=requested_field_names,
            filter_func=lambda db_columns,timestamp_start,timestamp_end : TrackerData.select(*db_columns).where(TrackerData.timestamp.between(timestamp_start, timestamp_end), TrackerData.rover_id==rover_id_parsed),
            filter_args=[timestamp_start, timestamp_end]
        )

    # Insert one or more data records into the database
    def insert_records(self, authentication_enabled, api_key, records):
        if authentication_enabled:
            self.validate_api_key(api_key)

        valid_record_count = 0
        duplicate_record_count = 0
        invalid_record_count = 0

        # Contains a list of outcomes for the ingestion of each record
        ingestion_log = []

        for record_index in range(len(records)):
            record = records[record_index]

            # Perform verification in incoming data
            current_record_exceptions = []

            # Check that the field names are valid in the data model (otherwise exeption thrown)
            try:
                self.field_names_to_fields(record.keys())
            except BadRequestError as e:
                current_record_exceptions.append(f"Record {record_index} invalid: {str(e)}")

            # Check that all the required fields are present
            try:
                self.validate_required_fields(record)
            except BadRequestError as e:
                current_record_exceptions.append(f"Record {record_index} invalid: {str(e)}")

            # Validate each present field
            if "rover_id" in record:
                try:
                    self.validate_rover_id(record["rover_id"])
                except BadRequestError as e:
                    current_record_exceptions.append(f"Record {record_index} invalid: {str(e)}")

            if "timestamp" in record:
                try:
                    self.validate_timestamp(record["timestamp"], "timestamp")
                except BadRequestError as e:
                    current_record_exceptions.append(f"Record {record_index} invalid: {str(e)}")

            if "longitude" in record:
                try:
                    self.validate_double(record["longitude"], "longitude")
                except BadRequestError as e:
                    current_record_exceptions.append(f"Record {record_index} invalid: {str(e)}")

            if "latitude" in record:
                try:
                    self.validate_double(record["latitude"], "latitude")
                except BadRequestError as e:
                    current_record_exceptions.append(f"Record {record_index} invalid: {str(e)}")

            if "altitude" in record:
                try:
                    self.validate_double(record["altitude"], "altitude")
                except BadRequestError as e:
                    current_record_exceptions.append(f"Record {record_index} invalid: {str(e)}")

            if "quality" in record:
                try:
                    self.validate_integer(record["quality"], "quality")
                except BadRequestError as e:
                    current_record_exceptions.append(f"Record {record_index} invalid: {str(e)}")

            if "hdop" in record:
                try:
                    self.validate_double(record["hdop"], "hdop")
                except BadRequestError as e:
                    current_record_exceptions.append(f"Record {record_index} invalid: {str(e)}")

            if "sats" in record:
                try:
                    self.validate_integer(record["sats"], "sats")
                except BadRequestError as e:
                    current_record_exceptions.append(f"Record {record_index} invalid: {str(e)}")

            if "temperature" in record:
                try:
                    self.validate_double(record["temperature"], "temperature")
                except BadRequestError as e:
                    current_record_exceptions.append(f"Record {record_index} invalid: {str(e)}")

            # If there are errors raised with the current record
            if current_record_exceptions:
                # Add the current list of record errors to the overall list
                ingestion_log += current_record_exceptions
                invalid_record_count += 1
            else:
                # Insert incoming data
                try:
                    # Instantiate a new record, populate its fields and then insert it into the table
                    # ** operator unpacks dictionary record into named argument form
                    TrackerData.create(**record)
                    ingestion_log.append(f"Record {record_index} valid.")
                    valid_record_count += 1
                except IntegrityError:
                    ingestion_log.append(f"Record {record_index} duplicated.")
                    duplicate_record_count += 1

        return valid_record_count, duplicate_record_count, invalid_record_count, ingestion_log

    # Get a list of the registered rover_ids + their glaciers
    def list_rovers(self, hide_unused):
        # Determines if we should include rovers with no associated records in the output (aka unused rovers)
        if hide_unused == None:
            rovers = TrackerDevices.select(TrackerDevices.rover_id, TrackerDevices.Glacier)
        else:
            rovers = TrackerDevices.select(TrackerDevices.rover_id, TrackerDevices.Glacier).join(TrackerData, JOIN.RIGHT_OUTER, on=(TrackerData.rover_id == TrackerDevices.rover_id)).group_by(TrackerData.rover_id)

        # Sort on the rover_ids, ascending numerically
        rovers_array = [{"rover_id": r.rover_id, "glacier": r.Glacier} for r in rovers]
        rovers_array.sort(key=lambda r : int(str(r["rover_id"])))

        # Convert these records into a JSON array
        return json.dumps(rovers_array, indent=2, default=str)

    # Convert a list of field names to the corresponding data model classes
    def field_names_to_fields(self, field_names):
        try:
            return [TrackerData.get_column_map()[field_name] for field_name in field_names]
        except KeyError as field_name:
            if field_name == "":
                raise BadRequestError("A field is blank.")
            raise BadRequestError(f"The requested field {field_name} does not exist.")

    # Get the minimum timestamp from the db
    def get_timestamp_min(self, rover_id):
        rover_id_parsed = self.validate_rover_id(rover_id)
        timestamp_min_records = TrackerData.select(fn.MIN(TrackerData.timestamp)).where(TrackerData.rover_id==rover_id_parsed).dicts()

        try:
            # Format the datetime as an ISO string
            timestamp_min = {"timestamp": timestamp_min_records[0]["timestamp"].isoformat()}
        except AttributeError:
            raise BadRequestError(f"The rover_id has no existing data records associated with it.")

        return timestamp_min

    # Get the maximum timestamp from the db
    def get_timestamp_max(self, rover_id):
        rover_id_parsed = self.validate_rover_id(rover_id)
        timestamp_max_records = TrackerData.select(fn.MAX(TrackerData.timestamp)).where(TrackerData.rover_id==rover_id_parsed).dicts()

        try:
            # Format the datetime as an ISO string
            timestamp_max = {"timestamp": timestamp_max_records[0]["timestamp"].isoformat()}
        except AttributeError:
            raise BadRequestError("The rover_id has no existing data records associated with it.")

        return timestamp_max

    # Checks if the request API key has been registered in the database
    def validate_api_key(self, api_key):
        # Hash the API key, as they are stored hashed within the database
        hash_gen = hashlib.sha512()
        hash_gen.update(api_key.encode('utf-8'))
        api_key_hash = hash_gen.hexdigest()

        # The IDs of registered API keys that match the provided key
        matching_api_key_ids = ApiKeys.select(ApiKeys.id).where(ApiKeys.api_key==api_key_hash).dicts()
        
        # Reject the request if no registered API keys match the provided key
        if len(matching_api_key_ids) == 0:
            raise BadRequestError("The API key is not registered.")

    # Perform checks on the rover_id to make sure it is valid/exists in the db
    def validate_rover_id(self, rover_id):
        # Verify that the rover id was provided
        if not rover_id:
            raise BadRequestError("The rover_id is required.")
        
        # Verify that the rover id is a valid integer
        try:
            rover_id_parsed = int(rover_id)
        except ValueError:
            raise BadRequestError("The rover_id is not a valid integer.")

        # Check to see if this rover_id is registered to a rover
        devices_with_rover_id = TrackerDevices.select().where(TrackerDevices.rover_id == rover_id_parsed)
        if len(devices_with_rover_id) == 0:
            raise BadRequestError("The rover_id is not registered to an existing rover.")

        return rover_id_parsed

    # Ensure a given value is matches ISO timestamp format
    def validate_timestamp(self, timestamp_val, timestamp_name):
        try:
            datetime.datetime.fromisoformat(timestamp_val)
        except ValueError:
            raise BadRequestError(f"The {timestamp_name} is not a valid datetime.")

    # Ensure a given value is a decimal number (ie. compatible with double format for MySQL)
    def validate_double(self, double_val, double_name):
        try:
            float(double_val)
        except ValueError:
            raise BadRequestError(f"The {double_name} is not a valid double.")

    # Ensure a given value is an integer number
    def validate_integer(self, integer_val, integer_name):
        try:
            int(integer_val)
        except ValueError:
            raise BadRequestError(f"The {integer_name} is not a valid integer.")

    # Ensure a given record contains all the required fields for ingestion
    def validate_required_fields(self, record):
        # Retrieve a list of the field names that were not included in the record
        absent_field_names = [field_name for field_name in TrackerData.get_column_map().keys() if field_name not in record.keys()]
        for field_name in absent_field_names:
            # Required fields are labelled null (don't include auto_increment fields as they cannot be ingested)
            if TrackerData.get_column_map()[field_name].null and not TrackerData.get_column_map()[field_name].auto_increment:
                raise BadRequestError(f"The {field_name} is required.")
    
    # Close the database connection
    def close_db(self):
        db.close()