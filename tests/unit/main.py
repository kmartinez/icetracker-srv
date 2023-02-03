import tests.unit.database as db

import unittest
import requests

RETRIEIVE_URL = "http://localhost/api/retrieve"
INGEST_URL = "http://localhost/api/ingest"

class TestQueryMethods(unittest.TestCase):
    # Hard resets the database before any unit testing begins
    def setUpClass():
        database = db.Database()
        database.hard_reset()

    # Soft resets the database before each unit test
    def setup_database(self):
        database = db.Database()
        database.soft_reset()

        return database

    # Filter by rover_id
    def test_retrieve_rover_id_filter_1(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '1', 'Portswood Glacier 1', 'The one and only glacier in Southern England')")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 12:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (2, '2', 'Portswood Glacier 2', 'The one and only glacier in Southern England')")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (2, '2000-01-02 12:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
            connection.commit()

        expected_response_json = [{
            "rover_id": 2,
            "timestamp": "2000-01-02 12:00:00"
        }]

        # TEST
        api_response = requests.get(
            url=RETRIEIVE_URL,
            params={
                "rover_id": 2,
                "requested_fields": [
                    "rover_id",
                    "timestamp"
                ]
            }
        )

        self.assertEqual(api_response.json(), expected_response_json)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Filter by rover_id (not provided)
    def test_retrieve_rover_id_filter_2(self):
        # SET UP
        database = self.setup_database()

        expected_response_text = "The rover_id is required."

        # TEST
        api_response = requests.get(
            url=RETRIEIVE_URL,
            params={}
        )

        self.assertEqual(api_response.text, expected_response_text)
        self.assertEqual(api_response.status_code, requests.codes.bad)

    # Filter by rover_id (not a valid integer - string instead)
    def test_retrieve_rover_id_filter_3(self):
        # SET UP
        database = self.setup_database()

        expected_response_text = "The rover_id is not a valid integer."

        # TEST
        api_response = requests.get(
            url=RETRIEIVE_URL,
            params={
                "rover_id": "foobar" # Not an integer value
            }
        )

        self.assertEqual(api_response.text, expected_response_text)
        self.assertEqual(api_response.status_code, requests.codes.bad)

    # Filter by rover_id (not registered to a rover)
    def test_retrieve_rover_id_filter_5(self):
        # SET UP
        database = self.setup_database()

        expected_response_text = "The rover_id is not registered to an existing rover."

        # TEST
        api_response = requests.get(
            url=RETRIEIVE_URL,
            params={
                "rover_id": 1
            }
        )

        self.assertEqual(api_response.text, expected_response_text)
        self.assertEqual(api_response.status_code, requests.codes.bad)

    # Filter between 2 timestamps
    def test_retrieve_timestamp_filter_1(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '1', 'Portswood Glacier 1', 'The one and only glacier in Southern England')")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 12:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 13:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 14:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 15:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
            connection.commit()

        expected_response_json = [
            {
                "rover_id": 1,
                "timestamp": "2000-01-01 13:00:00"
            },
            {
                "rover_id": 1,
                "timestamp": "2000-01-01 14:00:00"
            }
        ]

        # TEST
        api_response = requests.get(
            url=RETRIEIVE_URL,
            params={
                "rover_id": 1,
                "timestamp_start": "2000-01-01 12:30:00",
                "timestamp_end": "2000-01-01 14:30:00",
                "requested_fields": [
                    "rover_id",
                    "timestamp"
                ]
            }
        )

        self.assertEqual(api_response.json(), expected_response_json)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Filter between 2 timestamps (inclusivity check)
    def test_retrieve_timestamp_filter_2(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '1', 'Portswood Glacier 1', 'The one and only glacier in Southern England')")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 12:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 13:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 14:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 15:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
            connection.commit()

        expected_response_json = [
            {
                "rover_id": 1,
                "timestamp": "2000-01-01 13:00:00"
            },
            {
                "rover_id": 1,
                "timestamp": "2000-01-01 14:00:00"
            }
        ]

        # TEST
        api_response = requests.get(
            url=RETRIEIVE_URL,
            params={
                "rover_id": 1,
                "timestamp_start": "2000-01-01 13:00:00",
                "timestamp_end": "2000-01-01 14:00:00",
                "requested_fields": [
                    "rover_id",
                    "timestamp"
                ]
            }
        )

        self.assertEqual(api_response.json(), expected_response_json)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Filter between 2 timestamps (out-of-bounds check)
    def test_retrieve_timestamp_filter_3(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '1', 'Portswood Glacier 1', 'The one and only glacier in Southern England')")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 12:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 13:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
            connection.commit()

        expected_response_json = []

        # TEST
        api_response = requests.get(
            url=RETRIEIVE_URL,
            params={
                "rover_id": 1,
                "timestamp_start": "2000-01-01 14:00:00",
                "timestamp_end": "2000-01-01 15:00:00",
                "requested_fields": [
                    "rover_id",
                    "timestamp"
                ]
            }
        )

        self.assertEqual(api_response.json(), expected_response_json)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Filter by timestamp_start
    def test_retrieve_timestamp_filter_4(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '1', 'Portswood Glacier 1', 'The one and only glacier in Southern England')")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 12:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 13:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 14:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
            connection.commit()

        expected_response_json = [
            {
                "rover_id": 1,
                "timestamp": "2000-01-01 13:00:00"
            },
            {
                "rover_id": 1,
                "timestamp": "2000-01-01 14:00:00"
            }
        ]

        # TEST
        api_response = requests.get(
            url=RETRIEIVE_URL,
            params={
                "rover_id": 1,
                "timestamp_start": "2000-01-01 12:30:00",
                "requested_fields": [
                    "rover_id",
                    "timestamp"
                ]
            }
        )

        self.assertEqual(api_response.json(), expected_response_json)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Filter by timestamp_start (inclusivity check)
    def test_retrieve_timestamp_filter_5(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '1', 'Portswood Glacier 1', 'The one and only glacier in Southern England')")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 12:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 13:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 14:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
            connection.commit()

        expected_response_json = [
            {
                "rover_id": 1,
                "timestamp": "2000-01-01 13:00:00"
            },
            {
                "rover_id": 1,
                "timestamp": "2000-01-01 14:00:00"
            }
        ]

        # TEST
        api_response = requests.get(
            url=RETRIEIVE_URL,
            params={
                "rover_id": 1,
                "timestamp_start": "2000-01-01 13:00:00",
                "requested_fields": [
                    "rover_id",
                    "timestamp"
                ]
            }
        )

        self.assertEqual(api_response.json(), expected_response_json)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Filter by timestamp_start (out-of-bounds check)
    def test_retrieve_timestamp_filter_6(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '1', 'Portswood Glacier 1', 'The one and only glacier in Southern England')")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 12:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 13:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
            connection.commit()

        expected_response_json = []

        # TEST
        api_response = requests.get(
            url=RETRIEIVE_URL,
            params={
                "rover_id": 1,
                "timestamp_start": "2000-01-01 14:00:00",
                "requested_fields": [
                    "rover_id",
                    "timestamp"
                ]
            }
        )

        self.assertEqual(api_response.json(), expected_response_json)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Filter by timestamp_end
    def test_retrieve_timestamp_filter_7(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '1', 'Portswood Glacier 1', 'The one and only glacier in Southern England')")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 12:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 13:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 14:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
            connection.commit()

        expected_response_json = [
            {
                "rover_id": 1,
                "timestamp": "2000-01-01 12:00:00"
            },
            {
                "rover_id": 1,
                "timestamp": "2000-01-01 13:00:00"
            }
        ]

        # TEST
        api_response = requests.get(
            url=RETRIEIVE_URL,
            params={
                "rover_id": 1,
                "timestamp_end": "2000-01-01 13:30:00",
                "requested_fields": [
                    "rover_id",
                    "timestamp"
                ]
            }
        )

        self.assertEqual(api_response.json(), expected_response_json)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Filter by timestamp_end (inclusivity check)
    def test_retrieve_timestamp_filter_8(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '1', 'Portswood Glacier 1', 'The one and only glacier in Southern England')")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 12:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 13:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 14:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
            connection.commit()

        expected_response_json = [
            {
                "rover_id": 1,
                "timestamp": "2000-01-01 12:00:00"
            },
            {
                "rover_id": 1,
                "timestamp": "2000-01-01 13:00:00"
            }
        ]

        # TEST
        api_response = requests.get(
            url=RETRIEIVE_URL,
            params={
                "rover_id": 1,
                "timestamp_end": "2000-01-01 13:00:00",
                "requested_fields": [
                    "rover_id",
                    "timestamp"
                ]
            }
        )

        self.assertEqual(api_response.json(), expected_response_json)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Filter by timestamp_end (out-of-bounds check)
    def test_retrieve_timestamp_filter_9(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '1', 'Portswood Glacier 1', 'The one and only glacier in Southern England')")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 12:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 13:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
            connection.commit()

        expected_response_json = []

        # TEST
        api_response = requests.get(
            url=RETRIEIVE_URL,
            params={
                "rover_id": 1,
                "timestamp_end": "2000-01-01 11:00:00",
                "requested_fields": [
                    "rover_id",
                    "timestamp"
                ]
            }
        )

        self.assertEqual(api_response.json(), expected_response_json)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Filter by timestamp_start (not a valid integer - string instead)
    def test_retrieve_timestamp_filter_10(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '1', 'Portswood Glacier 1', 'The one and only glacier in Southern England')")
            connection.commit()

        expected_response_text = "The timestamp_start is not a valid datetime."

        # TEST
        api_response = requests.get(
            url=RETRIEIVE_URL,
            params={
                "rover_id": 1,
                "timestamp_start": "foobar"
            }
        )

        self.assertEqual(api_response.text, expected_response_text)
        self.assertEqual(api_response.status_code, requests.codes.bad)

    # Filter by timestamp_end (not a valid integer - string instead)
    def test_retrieve_timestamp_filter_11(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '1', 'Portswood Glacier 1', 'The one and only glacier in Southern England')")
            connection.commit()

        expected_response_text = "The timestamp_end is not a valid datetime."

        # TEST
        api_response = requests.get(
            url=RETRIEIVE_URL,
            params={
                "rover_id": 1,
                "timestamp_end": "foobar"
            }
        )

        self.assertEqual(api_response.text, expected_response_text)
        self.assertEqual(api_response.status_code, requests.codes.bad)

    # Filter between 2 timestamps (end earlier than the start)
    def test_retrieve_timestamp_filter_12(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '1', 'Portswood Glacier 1', 'The one and only glacier in Southern England')")
            connection.commit()

        expected_response_text = "The timestamp_start is at a later date than the timestamp_end."

        # TEST
        api_response = requests.get(
            url=RETRIEIVE_URL,
            params={
                "rover_id": 1,
                "timestamp_start": "2000-01-02 12:00:00",
                "timestamp_end": "2000-01-01 12:00:00"
            }
        )

        self.assertEqual(api_response.text, expected_response_text)
        self.assertEqual(api_response.status_code, requests.codes.bad)

    # Requested fields (all by default)
    def test_retrieve_requested_fields_1(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 12:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 13:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
            connection.commit()

        expected_response_json_keys = [
            "id",
            "rover_id",
            "timestamp",
            "longitude",
            "latitude",
            "altitude",
            "quality",
            "hdop",
            "sats",
            "temperature",
            "displacement",
            "velocity"
        ]

        # TEST
        api_response = requests.get(
            url=RETRIEIVE_URL,
            params={
                "rover_id": 1
            }
        )

        self.assertEqual(list(api_response.json()[0].keys()), expected_response_json_keys)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Requested fields (non calculated)
    def test_retrieve_requested_fields_2(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 12:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
            connection.commit()

        expected_response_json_keys = [
            "id",
            "rover_id",
            "timestamp",
            "longitude",
            "latitude",
            "altitude",
            "quality",
            "hdop",
            "sats",
            "temperature"
        ]

        # TEST
        api_response = requests.get(
            url=RETRIEIVE_URL,
            params={
                "rover_id": 1,
                "requested_fields": [
                    "id",
                    "rover_id",
                    "timestamp",
                    "longitude",
                    "latitude",
                    "altitude",
                    "quality",
                    "hdop",
                    "sats",
                    "temperature"
                ]
            }
        )

        self.assertEqual(list(api_response.json()[0].keys()), expected_response_json_keys)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Requested fields (random selection)
    def test_retrieve_requested_fields_3(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 12:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
            connection.commit()

        expected_response_json_keys = [
            "rover_id",
            "latitude",
            "quality",
            "hdop",
            "temperature"
        ]

        # TEST
        api_response = requests.get(
            url=RETRIEIVE_URL,
            params={
                "rover_id": 1,
                "requested_fields": [
                    "rover_id",
                    "latitude",
                    "quality",
                    "hdop",
                    "temperature"
                ]
            }
        )

        self.assertEqual(list(api_response.json()[0].keys()), expected_response_json_keys)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Requested fields (duplicate field ignored)
    def test_retrieve_requested_fields_4(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 12:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
            connection.commit()

        expected_response_json_keys = [
            "id",
        ]

        # TEST
        api_response = requests.get(
            url=RETRIEIVE_URL,
            params={
                "rover_id": 1,
                "requested_fields": [
                    "id",
                    "id"
                ]
            }
        )

        self.assertEqual(list(api_response.json()[0].keys()), expected_response_json_keys)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Requested fields (non existent field)
    def test_retrieve_requested_fields_5(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 12:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
            connection.commit()

        expected_response_text = "The requested field 'foobar' does not exist."

        # TEST
        api_response = requests.get(
            url=RETRIEIVE_URL,
            params={
                "rover_id": 1,
                "requested_fields": [
                    "foobar"
                ]
            }
        )

        self.assertEqual(api_response.text, expected_response_text)
        self.assertEqual(api_response.status_code, requests.codes.bad)

    # Requested fields (retrieve velocity from a single record)
    def test_retrieve_requested_fields_6(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 12:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
            connection.commit()

        expected_response_text = "Not possible to calculate velocity from one record."

        # TEST
        api_response = requests.get(
            url=RETRIEIVE_URL,
            params={
                "rover_id": 1,
                "requested_fields": "velocity"
            }
        )

        self.assertEqual(api_response.text, expected_response_text)
        self.assertEqual(api_response.status_code, requests.codes.bad)

    # Data format (defaults to JSON)
    def test_retrieve_data_format_1(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 12:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
            connection.commit()

        expected_response_json = [{
            "rover_id": 1,
            "timestamp": "2000-01-01 12:00:00"
        }]

        # TEST
        api_response = requests.get(
            url=RETRIEIVE_URL,
            params={
                "rover_id": 1,
                "requested_fields": [
                    "rover_id",
                    "timestamp"
                ]
            }
        )

        self.assertEqual(api_response.json(), expected_response_json)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Data format (JSON)
    def test_retrieve_data_format_2(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 12:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
            connection.commit()

        expected_response_json = [{
            "rover_id": 1,
            "timestamp": "2000-01-01 12:00:00"
        }]

        # TEST
        api_response = requests.get(
            url=RETRIEIVE_URL,
            params={
                "rover_id": 1,
                "requested_fields": [
                    "rover_id",
                    "timestamp"
                ],
                "data_format": "json"
            }
        )

        self.assertEqual(api_response.json(), expected_response_json)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Data format (CSV)
    def test_retrieve_data_format_3(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 12:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
            connection.commit()

        expected_response_csv = "rover_id,timestamp\n1,2000-01-01 12:00:00\n"

        # TEST
        api_response = requests.get(
            url=RETRIEIVE_URL,
            params={
                "rover_id": 1,
                "requested_fields": [
                    "rover_id",
                    "timestamp"
                ],
                "data_format": "csv"
            }
        )

        self.assertEqual(api_response.text, expected_response_csv)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Data format (unsupported format)
    def test_retrieve_data_format_4(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 12:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
            connection.commit()

        expected_response_csv = "The requested data_format is not supported."

        # TEST
        api_response = requests.get(
            url=RETRIEIVE_URL,
            params={
                "rover_id": 1,
                "data_format": "foobar"
            }
        )

        self.assertEqual(api_response.text, expected_response_csv)
        self.assertEqual(api_response.status_code, requests.codes.bad)

    # Ingest all possible fields
    def test_ingest_all_fields(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
            connection.commit()

        expected_response_text = "Received 1 records.\n\nValid: 1\nDuplicated: 0\nInvalid: 0\n\nRecord 0 valid."

        # TEST
        api_response = requests.post(
            url=INGEST_URL,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "api_key": "testkey",
                "records": [
                    {
                        "rover_id": 1,
                        "timestamp": "2000-01-01 12:00:00",
                        "longitude": 1.0,
                        "latitude": 1.0,
                        "altitude": 1.0,
                        "quality": 1,
                        "hdop": 1.0,
                        "sats": 1,
                        "temperature": 1.0
                    }
                ]
            }
        )

        self.assertEqual(api_response.text, expected_response_text)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Ingest multiple valid records at once
    def test_ingest_multiple_valid_records(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
            connection.commit()

        expected_response_text = "Received 3 records.\n\nValid: 3\nDuplicated: 0\nInvalid: 0\n\nRecord 0 valid.\nRecord 1 valid.\nRecord 2 valid."

        # TEST
        api_response = requests.post(
            url=INGEST_URL,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "api_key": "testkey",
                "records": [
                    {
                        "rover_id": 1,
                        "timestamp": "2000-01-01 12:00:00",
                        "longitude": 1.0,
                        "latitude": 1.0,
                        "altitude": 1.0,
                        "quality": 1,
                        "hdop": 1.0,
                        "sats": 1,
                        "temperature": 1.0
                    },
                    {
                        "rover_id": 1,
                        "timestamp": "2000-01-01 13:00:00",
                        "longitude": 1.0,
                        "latitude": 1.0,
                        "altitude": 1.0,
                        "quality": 1,
                        "hdop": 1.0,
                        "sats": 1,
                        "temperature": 1.0
                    },
                    {
                        "rover_id": 1,
                        "timestamp": "2000-01-01 14:00:00",
                        "longitude": 1.0,
                        "latitude": 1.0,
                        "altitude": 1.0,
                        "quality": 1,
                        "hdop": 1.0,
                        "sats": 1,
                        "temperature": 1.0
                    }
                ]
            }
        )

        self.assertEqual(api_response.text, expected_response_text)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Ingest duplicated record
    def test_ingest_duplicated_record(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
                cursor.execute("INSERT INTO tracker_data (rover_id, timestamp, longitude, latitude, altitude, quality, hdop, sats, temperature) VALUES (1, '2000-01-01 12:00:00', 1.0, 1.0, 1.0, 1, 1.0, 1, 1.0)")
            connection.commit()

        expected_response_text = "Received 1 records.\n\nValid: 0\nDuplicated: 1\nInvalid: 0\n\nRecord 0 duplicated."

        # TEST
        api_response = requests.post(
            url=INGEST_URL,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "api_key": "testkey",
                "records": [
                    {
                        "rover_id": 1,
                        "timestamp": "2000-01-01 12:00:00",
                        "longitude": 1.0,
                        "latitude": 1.0,
                        "altitude": 1.0,
                        "quality": 1,
                        "hdop": 1.0,
                        "sats": 1,
                        "temperature": 1.0
                    }
                ]
            }
        )

        self.assertEqual(api_response.text, expected_response_text)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Ingest valid record followed by the same (now duplicated) record
    def test_ingest_duplicated_record_in_single_request(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
            connection.commit()

        expected_response_text = "Received 2 records.\n\nValid: 1\nDuplicated: 1\nInvalid: 0\n\nRecord 0 valid.\nRecord 1 duplicated."

        # TEST
        api_response = requests.post(
            url=INGEST_URL,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "api_key": "testkey",
                "records": [
                    {
                        "rover_id": 1,
                        "timestamp": "2000-01-01 12:00:00",
                        "longitude": 1.0,
                        "latitude": 1.0,
                        "altitude": 1.0,
                        "quality": 1,
                        "hdop": 1.0,
                        "sats": 1,
                        "temperature": 1.0
                    },
                    {
                        "rover_id": 1,
                        "timestamp": "2000-01-01 12:00:00",
                        "longitude": 1.0,
                        "latitude": 1.0,
                        "altitude": 1.0,
                        "quality": 1,
                        "hdop": 1.0,
                        "sats": 1,
                        "temperature": 1.0
                    }
                ]
            }
        )

        self.assertEqual(api_response.text, expected_response_text)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Ingest non-existent field
    def test_ingest_non_existent_field(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
            connection.commit()

        expected_response_text = "Received 1 records.\n\nValid: 0\nDuplicated: 0\nInvalid: 1\n\nRecord 0 invalid: The requested field 'foobar' does not exist."

        # TEST
        api_response = requests.post(
            url=INGEST_URL,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "api_key": "testkey",
                "records": [
                    {
                        "rover_id": 1,
                        "timestamp": "2000-01-01 12:00:00",
                        "longitude": 1.0,
                        "latitude": 1.0,
                        "altitude": 1.0,
                        "sats": 1,
                        "foobar": "baz"
                    }
                ]
            }
        )

        self.assertEqual(api_response.text, expected_response_text)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Ingest required fields
    def test_ingest_required_fields(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
            connection.commit()

        expected_response_text = "Received 1 records.\n\nValid: 1\nDuplicated: 0\nInvalid: 0\n\nRecord 0 valid."

        # TEST
        api_response = requests.post(
            url=INGEST_URL,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "api_key": "testkey",
                "records": [
                    {
                        "rover_id": 1,
                        "timestamp": "2000-01-01 12:00:00",
                        "longitude": 1.0,
                        "latitude": 1.0,
                        "altitude": 1.0,
                        "sats": 1
                    }
                ]
            }
        )

        self.assertEqual(api_response.text, expected_response_text)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Ingest missing required field rover_id
    def test_ingest_missing_required_field_rover_id(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
            connection.commit()

        expected_response_text = "Received 1 records.\n\nValid: 0\nDuplicated: 0\nInvalid: 1\n\nRecord 0 invalid: The rover_id is required."

        # TEST
        api_response = requests.post(
            url=INGEST_URL,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "api_key": "testkey",
                "records": [
                    {
                        "timestamp": "2000-01-01 12:00:00",
                        "longitude": 1.0,
                        "latitude": 1.0,
                        "altitude": 1.0,
                        "sats": 1
                    }
                ]
            }
        )

        self.assertEqual(api_response.text, expected_response_text)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Ingest missing required field timestamp
    def test_ingest_missing_required_field_timestamp(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
            connection.commit()

        expected_response_text = "Received 1 records.\n\nValid: 0\nDuplicated: 0\nInvalid: 1\n\nRecord 0 invalid: The timestamp is required."

        # TEST
        api_response = requests.post(
            url=INGEST_URL,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "api_key": "testkey",
                "records": [
                    {
                        "rover_id": 1,
                        "longitude": 1.0,
                        "latitude": 1.0,
                        "altitude": 1.0,
                        "sats": 1
                    }
                ]
            }
        )

        self.assertEqual(api_response.text, expected_response_text)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Ingest missing required field longitude
    def test_ingest_missing_required_field_longitude(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
            connection.commit()

        expected_response_text = "Received 1 records.\n\nValid: 0\nDuplicated: 0\nInvalid: 1\n\nRecord 0 invalid: The longitude is required."

        # TEST
        api_response = requests.post(
            url=INGEST_URL,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "api_key": "testkey",
                "records": [
                    {
                        "rover_id": 1,
                        "timestamp": "2000-01-01 12:00:00",
                        "latitude": 1.0,
                        "altitude": 1.0,
                        "sats": 1
                    }
                ]
            }
        )

        self.assertEqual(api_response.text, expected_response_text)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Ingest missing required field latitude
    def test_ingest_missing_required_field_latitude(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
            connection.commit()

        expected_response_text = "Received 1 records.\n\nValid: 0\nDuplicated: 0\nInvalid: 1\n\nRecord 0 invalid: The latitude is required."

        # TEST
        api_response = requests.post(
            url=INGEST_URL,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "api_key": "testkey",
                "records": [
                    {
                        "rover_id": 1,
                        "timestamp": "2000-01-01 12:00:00",
                        "longitude": 1.0,
                        "altitude": 1.0,
                        "sats": 1
                    }
                ]
            }
        )

        self.assertEqual(api_response.text, expected_response_text)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Ingest missing required field altitude
    def test_ingest_missing_required_field_altitude(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
            connection.commit()

        expected_response_text = "Received 1 records.\n\nValid: 0\nDuplicated: 0\nInvalid: 1\n\nRecord 0 invalid: The altitude is required."

        # TEST
        api_response = requests.post(
            url=INGEST_URL,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "api_key": "testkey",
                "records": [
                    {
                        "rover_id": 1,
                        "timestamp": "2000-01-01 12:00:00",
                        "longitude": 1.0,
                        "latitude": 1.0,
                        "sats": 1
                    }
                ]
            }
        )

        self.assertEqual(api_response.text, expected_response_text)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Ingest missing required field sats
    def test_ingest_missing_required_field_sats(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
            connection.commit()

        expected_response_text = "Received 1 records.\n\nValid: 0\nDuplicated: 0\nInvalid: 1\n\nRecord 0 invalid: The sats is required."

        # TEST
        api_response = requests.post(
            url=INGEST_URL,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "api_key": "testkey",
                "records": [
                    {
                        "rover_id": 1,
                        "timestamp": "2000-01-01 12:00:00",
                        "longitude": 1.0,
                        "latitude": 1.0,
                        "altitude": 1.0
                    }
                ]
            }
        )

        self.assertEqual(api_response.text, expected_response_text)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Ingest a timestamp in invalid datetime format (integer)
    def test_ingest_timestamp_invalid_datetime_1(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
            connection.commit()

        expected_response_text = "Received 1 records.\n\nValid: 0\nDuplicated: 0\nInvalid: 1\n\nRecord 0 invalid: The timestamp is not a valid datetime."

        # TEST
        api_response = requests.post(
            url=INGEST_URL,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "api_key": "testkey",
                "records": [
                    {
                        "rover_id": 1,
                        "timestamp": 99999,
                        "longitude": 1.0,
                        "latitude": 1.0,
                        "altitude": 1.0,
                        "sats": 1
                    }
                ]
            }
        )

        self.assertEqual(api_response.text, expected_response_text)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Ingest a timestamp in invalid datetime format (string)
    def test_ingest_timestamp_invalid_datetime_2(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
            connection.commit()

        expected_response_text = "Received 1 records.\n\nValid: 0\nDuplicated: 0\nInvalid: 1\n\nRecord 0 invalid: The timestamp is not a valid datetime."

        # TEST
        api_response = requests.post(
            url=INGEST_URL,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "api_key": "testkey",
                "records": [
                    {
                        "rover_id": 1,
                        "timestamp": "foobar",
                        "longitude": 1.0,
                        "latitude": 1.0,
                        "altitude": 1.0,
                        "sats": 1
                    }
                ]
            }
        )

        self.assertEqual(api_response.text, expected_response_text)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Ingest a timestamp in invalid datetime format (impossible datetime)
    def test_ingest_timestamp_invalid_datetime_3(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
            connection.commit()

        expected_response_text = "Received 1 records.\n\nValid: 0\nDuplicated: 0\nInvalid: 1\n\nRecord 0 invalid: The timestamp is not a valid datetime."

        # TEST
        api_response = requests.post(
            url=INGEST_URL,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "api_key": "testkey",
                "records": [
                    {
                        "rover_id": 1,
                        "timestamp": "9999-99-99 99:99:99",
                        "longitude": 1.0,
                        "latitude": 1.0,
                        "altitude": 1.0,
                        "sats": 1
                    }
                ]
            }
        )

        self.assertEqual(api_response.text, expected_response_text)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Ingest a timestamp before unix epoch time
    def test_ingest_timestamp_before_unix_epoch(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
            connection.commit()

        expected_response_text = "Received 1 records.\n\nValid: 1\nDuplicated: 0\nInvalid: 0\n\nRecord 0 valid."

        # TEST
        api_response = requests.post(
            url=INGEST_URL,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "api_key": "testkey",
                "records": [
                    {
                        "rover_id": 1,
                        "timestamp": "1969-01-01 12:00:00",
                        "longitude": 1.0,
                        "latitude": 1.0,
                        "altitude": 1.0,
                        "sats": 1
                    }
                ]
            }
        )

        self.assertEqual(api_response.text, expected_response_text)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Ingest a timestamp after y2038 bug time
    def test_ingest_timestamp_after_y2038_bug(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
            connection.commit()

        expected_response_text = "Received 1 records.\n\nValid: 1\nDuplicated: 0\nInvalid: 0\n\nRecord 0 valid."

        # TEST
        api_response = requests.post(
            url=INGEST_URL,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "api_key": "testkey",
                "records": [
                    {
                        "rover_id": 1,
                        "timestamp": "2039-01-01 12:00:00",
                        "longitude": 1.0,
                        "latitude": 1.0,
                        "altitude": 1.0,
                        "sats": 1
                    }
                ]
            }
        )

        self.assertEqual(api_response.text, expected_response_text)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Ingest a longitude in invalid double format (string)
    def test_ingest_longitude_invalid_double(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
            connection.commit()

        expected_response_text = "Received 1 records.\n\nValid: 0\nDuplicated: 0\nInvalid: 1\n\nRecord 0 invalid: The longitude is not a valid double."

        # TEST
        api_response = requests.post(
            url=INGEST_URL,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "api_key": "testkey",
                "records": [
                    {
                        "rover_id": 1,
                        "timestamp": "2000-01-01 12:00:00",
                        "longitude": "foobar",
                        "latitude": 1.0,
                        "altitude": 1.0,
                        "sats": 1
                    }
                ]
            }
        )

        self.assertEqual(api_response.text, expected_response_text)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Ingest a latitude in invalid double format (string)
    def test_ingest_latitude_invalid_double(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
            connection.commit()

        expected_response_text = "Received 1 records.\n\nValid: 0\nDuplicated: 0\nInvalid: 1\n\nRecord 0 invalid: The latitude is not a valid double."

        # TEST
        api_response = requests.post(
            url=INGEST_URL,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "api_key": "testkey",
                "records": [
                    {
                        "rover_id": 1,
                        "timestamp": "2000-01-01 12:00:00",
                        "longitude": 1.0,
                        "latitude": "foobar",
                        "altitude": 1.0,
                        "sats": 1
                    }
                ]
            }
        )

        self.assertEqual(api_response.text, expected_response_text)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Ingest a altitude in invalid double format (string)
    def test_ingest_altitude_invalid_double(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
            connection.commit()

        expected_response_text = "Received 1 records.\n\nValid: 0\nDuplicated: 0\nInvalid: 1\n\nRecord 0 invalid: The altitude is not a valid double."

        # TEST
        api_response = requests.post(
            url=INGEST_URL,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "api_key": "testkey",
                "records": [
                    {
                        "rover_id": 1,
                        "timestamp": "2000-01-01 12:00:00",
                        "longitude": 1.0,
                        "latitude": 1.0,
                        "altitude": "foobar",
                        "sats": 1
                    }
                ]
            }
        )

        self.assertEqual(api_response.text, expected_response_text)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Ingest a quality in invalid integer format (string)
    def test_ingest_quality_invalid_integer(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
            connection.commit()

        expected_response_text = "Received 1 records.\n\nValid: 0\nDuplicated: 0\nInvalid: 1\n\nRecord 0 invalid: The quality is not a valid integer."

        # TEST
        api_response = requests.post(
            url=INGEST_URL,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "api_key": "testkey",
                "records": [
                    {
                        "rover_id": 1,
                        "timestamp": "2000-01-01 12:00:00",
                        "longitude": 1.0,
                        "latitude": 1.0,
                        "altitude": 1.0,
                        "sats": 1,
                        "quality": "foobar"
                    }
                ]
            }
        )

        self.assertEqual(api_response.text, expected_response_text)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Ingest a hdop in invalid double format (string)
    def test_ingest_hdop_invalid_double(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
            connection.commit()

        expected_response_text = "Received 1 records.\n\nValid: 0\nDuplicated: 0\nInvalid: 1\n\nRecord 0 invalid: The hdop is not a valid double."

        # TEST
        api_response = requests.post(
            url=INGEST_URL,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "api_key": "testkey",
                "records": [
                    {
                        "rover_id": 1,
                        "timestamp": "2000-01-01 12:00:00",
                        "longitude": 1.0,
                        "latitude": 1.0,
                        "altitude": 1.0,
                        "sats": 1,
                        "hdop": "foobar"
                    }
                ]
            }
        )

        self.assertEqual(api_response.text, expected_response_text)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Ingest a sats in invalid integer format (string)
    def test_ingest_sats_invalid_integer(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
            connection.commit()

        expected_response_text = "Received 1 records.\n\nValid: 0\nDuplicated: 0\nInvalid: 1\n\nRecord 0 invalid: The sats is not a valid integer."

        # TEST
        api_response = requests.post(
            url=INGEST_URL,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "api_key": "testkey",
                "records": [
                    {
                        "rover_id": 1,
                        "timestamp": "2000-01-01 12:00:00",
                        "longitude": 1.0,
                        "latitude": 1.0,
                        "altitude": 1.0,
                        "sats": "foobar"
                    }
                ]
            }
        )

        self.assertEqual(api_response.text, expected_response_text)
        self.assertEqual(api_response.status_code, requests.codes.ok)

    # Ingest a temperature in invalid double format (string)
    def test_ingest_temperature_invalid_double(self):
        # SET UP
        database = self.setup_database()

        with database.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("USE iceland")
                cursor.execute("INSERT INTO tracker_devices (rover_id, imei, Glacier, Notes) VALUES (1, '9999', 'Portswood Glacier', 'The one and only glacier in Southern England')")
            connection.commit()

        expected_response_text = "Received 1 records.\n\nValid: 0\nDuplicated: 0\nInvalid: 1\n\nRecord 0 invalid: The temperature is not a valid double."

        # TEST
        api_response = requests.post(
            url=INGEST_URL,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "api_key": "testkey",
                "records": [
                    {
                        "rover_id": 1,
                        "timestamp": "2000-01-01 12:00:00",
                        "longitude": 1.0,
                        "latitude": 1.0,
                        "altitude": 1.0,
                        "sats": 1,
                        "temperature": "foobar"
                    }
                ]
            }
        )

        self.assertEqual(api_response.text, expected_response_text)
        self.assertEqual(api_response.status_code, requests.codes.ok)

if __name__ == "__main__":
    unittest.main()