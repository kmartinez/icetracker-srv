from flask import Flask, render_template, request, g
from flask_bootstrap import Bootstrap5
from flask_fontawesome import FontAwesome
from api.database import Database, BadRequestError

import json
import cbor2
import bleach

app = Flask(__name__)
bootstrap = Bootstrap5(app)
fonts = FontAwesome(app)

app.secret_key = "a secret key"


@app.route("/")
@app.route("/index")
def index():
    return render_template("graphs.html")


@app.route("/data")
def data():
    return render_template("data.html")


# Get a database connection
def get_db():
    if 'db' not in g:
        # Connect to the database
        g.db = Database(app.config["db_host"], app.config["db_port"])

    return g.db


# Wraps all routes to respond to bad requests with HTTP error 400
@app.errorhandler(BadRequestError)
def handle_error(error):
    # Return the error with a 400 status
    print(f"Response: {str(error)}")
    return bleach.clean(str(error)), 400


# Close the database connection
@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)

    if db is not None:
        db.close_db()


@app.route("/api/retrieve", methods=["GET"])
def retrieve():
    # Get values from HTTP request query params
    rover_id = request.args.get("rover_id")
    timestamp_start = request.args.get("timestamp_start")
    timestamp_end = request.args.get("timestamp_end")
    data_format = request.args.get("data_format")
    requested_fields = request.args.getlist("requested_fields")

    # Debug info
    print(f"Requesting records for rover {rover_id} between timestamps {timestamp_start} and {timestamp_end} ")
    print(f"Fields requested: {requested_fields}")

    # Query the DB for a list of matching records and sanitize them
    response = get_db().retrieve_records(data_format, requested_fields, rover_id, timestamp_start, timestamp_end)
    return bleach.clean(response)


@app.route("/api/ingest", methods=["POST"])
def ingest():
    # Ensure the request body has been set
    if request.data == b'':
        raise BadRequestError("The request has no body.")

    # Retrieve request body and converts JSON/CBOR into a Python dictionary
    try:
        # Supports JSON or CBOR (defaults to JSON)
        if request.mimetype == "application/cbor":
            body = cbor2.loads(request.data)
        else:
            body = json.loads(request.data)

    except (MemoryError, json.decoder.JSONDecodeError):
        raise BadRequestError("The request body is badly formatted.")


    # Get the API key from the request body (if authentication enabled)
    if app.config["authenticate_ingestion"]:
        authentication_enabled = True
        try:
            api_key = body["api_key"]
        except (KeyError, TypeError):
            raise BadRequestError("The request body contains no api_key key.")
    else:
        authentication_enabled = False
        api_key = ""

    # Get the new records from the request body
    try:
        records = body["records"]
    except (KeyError, TypeError):
        raise BadRequestError("The request body contains no records key.")

    # Sanitize newly ingested records for input
    # text based attacks e.g. XSS, SQL injection
    sanitized_records = [{key: bleach.clean(str(val)) for key, val in record.items()} for record in records]

    # Query the DB to insert the new records
    valid_record_count, duplicate_record_count, invalid_record_count, ingestion_log = get_db().insert_records(authentication_enabled, api_key, sanitized_records)

    response_msg = f"Received {len(sanitized_records)} records.\n"
    response_msg += "\n"
    response_msg += f"Valid: {valid_record_count}\n"
    response_msg += f"Duplicated: {duplicate_record_count}\n"
    response_msg += f"Invalid: {invalid_record_count}\n"
    response_msg += "\n"
    response_msg += "\n".join(ingestion_log)

    print(response_msg)
    return response_msg


@app.route("/api/query/rovers", methods=["GET"])
def query_rovers():
    # Get value from HTTP request query params
    hide_unused = request.args.get("hide_unused")

    # Get a list of the registered rovers
    return get_db().list_rovers(hide_unused)


@app.route("/api/query/timestamp_min", methods=["GET"])
def query_timestamp_min():
    # Get value from HTTP request query params
    rover_id = request.args.get("rover_id")

    # Get the first recorded timestamp for a specific rover_id
    return get_db().get_timestamp_min(rover_id)


@app.route("/api/query/timestamp_max", methods=["GET"])
def query_timestamp_max():
    # Get value from HTTP request query params
    rover_id = request.args.get("rover_id")

    # Get the last recorded timestamp for a specific rover_id
    return get_db().get_timestamp_max(rover_id)
