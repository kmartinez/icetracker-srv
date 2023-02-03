# Glacsweb API

This API allows retrieval and storage of data from Glacsweb basestations into a central database. All requests to the API are made to endpoints starting with `/api`.

## 1 Retrieval - Fetching existing data

Endpoint:
```
GET /api/retrieve
```

All responses from this endpoint will return an array of `record` objects.

Each `record` object in the array has:

| Field | Type | Description |
| - | - | - |
| `id` | Integer | A unique identifier for each record. |
| `rover_id` | Integer | A unique identifier for the rover device from which the readings came from. |
| `timestamp` | Datetime | Time/date at which the readings were taken. |
| `longitude` | Double | Longitude of basestation. |
| `latitude` | Double | Latitude of basestation. |
| `altitude` | Double | Altitude of basestation. |
| `quality` | Integer | Quality of signal. |
| `hdop` | Float | Horizontal Dilution of Precision. |
| `sats` | Integer | Number of satellites connected. |
| `temperature` | Float | Temperature reading from the basestation. |
| `displacement` | Float | Total displacemnt from the first reading requested. |
| `velocity` | Float | The velocity of the tracker. |

Full example response in JSON:

```json
[
    {
        "id": 32,
        "rover_id": 2,
        "timestamp": "2017-09-01 00:01:00",
        "longitude": -16.33418463,
        "latitude": 64.0937139,
        "altitude": 148.45,
        "quality": 4,
        "hdop": 1.0,
        "sats": 9,
        "temperature": 13.0,
        "displacement": 0.016115088975548267,
        "velocity": 18.39495895729398
    },
    {
        "id": 33,
        "rover_id": 2,
        "timestamp": "2017-09-01 03:01:00",
        "longitude": -16.33418479,
        "latitude": 64.0937139,
        "altitude": 148.44,
        "quality": 4,
        "hdop": 1.0,
        "sats": 11,
        "temperature": 13.1,
        "displacement": 0.013116919665866741,
        "velocity": 38.68106972469605
    }
]
```

### 1.1 Filtering by `rover_id`

Filters are applied via the use of query parameters (with the ?filter_name={{filter_value}} syntax in the url).

The filter the response to only readings from a single rover device, the `rover_id` query parameter is used.

Example request:
```
GET /api/retrieve
?rover_id={{rover id}}
HTTP/1.1
Host: <hostname>:<port>
```

Example response:

```json
[
    {
        "id": 25,
        "rover_id": 5,
            ...
        "temperature": 12.9
    },
    {
        "id": 26,
        "rover_id": 5,
            ...
        "temperature": 12.5
    },
    {
        "id": 27,
        "rover_id": 5,
            ...
        "temperature": 12.2
    }
]
```

Query parameter:

| Name | Type | Description | Example | Required |
| - | - | - | - | - |
| `rover_id` | Integer | A unique identifier for the rover device from which you require readings. | *2* | Yes |

Errors:

| HTTP code | Description |
| - | - |
| 400 | The `rover_id` is required. |
| 400 | The `rover_id` is not a valid integer. |
| 400 | The `rover_id` is not registered to an existing rover. |

### 1.2 Filtering between 2 timestamps

The filter the response to only records recorded within a specificied timeframe, the `timestamp_start` and `timestamp_end` query parameters are used.
Note that the `rover_id` filter is also present as it is required in all requests (see above section).

Example request:
```
GET /api/retrieve
?rover_id={{rover id}}
&timestamp_start={{starting timestamp}}
&timestamp_end={{ending timestamp}}
HTTP/1.1
Host: <hostname>:<port>
```

Example response:

```json
[
    {
        "id": 25,
            ...
        "timestamp": "2017-09-01 00:01:00",
            ...
        "temperature": 12.9
    },
    {
        "id": 26,
            ...
        "timestamp": "2017-09-01 03:01:00",
            ...
        "temperature": 12.5
    }
]
```

Query parameters:

| Name | Type | Description | Example | Required | Default |
| - | - | - | - | - | - |
| `timestamp_start` | ISO datetime | The time/date, after which to retrieve records from. | *2021-09-01T13:00:00* | No | Earliest possible time/date
| `timestamp_end` | ISO datetime | The time/date, before which to retrieve records from. | *2021-09-01T13:00:00* | No | Latest possible time/date

Errors:

| HTTP code | Description |
| - | - |
| 400 | The `timestamp_start` is not a valid datetime. |
| 400 | The `timestamp_end` is not a valid datetime. |
| 400 | The `timestamp_start` is at a later date than the `timestamp_end`. |

### 1.3 Specifying which fields to retrieve

To request a response containing only a subset of the fields stored in the database, the `&requested_fields=` query parameter is used.

Example request:
```
GET /api/retrieve
?rover_id={{rover id}}
&requested_fields={{field name A}}
&requested_fields={{field name B}}
&requested_fields={{field name C}}
HTTP/1.1
Host: <hostname>:<port>
```

Example response:

```json
[
    {
        "latitude": 64.0937107
        "longitude": -16.33418287
    },
    {
        "latitude": 64.09371393
        "longitude": -16.3341846
    },
    {
        "latitude": 64.0937139
        "longitude": -16.33418471
    }
]
```

Query parameters:

| Name | Type | Description | Example | Required | Default |
| - | - | - | - | - | - |
| `requested_fields` | String | The name of a field to be included in the output. | *hdop* | No | All fields

This parameter can be included multiple times to specify that several fields should be included in the response.

Errors:

| HTTP code | Description |
| - | - |
| 400 | The requested field '`{{field name}}`' does not exist. |
| 400 | Not possible to calculate velocity from one record. |

### 1.4 Selecting response data format

Example request:
```
GET /api/retrieve
?rover_id={{rover id}}
&data_format={{response format}}
HTTP/1.1
Host: <hostname>:<port>
```

Example response for `&data_format=json`:

```json
[
    {
        "id": 94,
            ...
        "temperature": 12.2
    },
    {
        "id": 95,
            ...
        "temperature": 12.4
    }
]
```

Example response for `&data_format=csv`:

```csv
id,rover_id,timestamp,longitude,latitude,altitude,quality,hdop,sats,temperature
94,2,2017-09-01 00:01:00,-16.33418463,64.0937139,148.45,4,10,12.2
95,2,2017-09-01 21:01:00,-16.33418453,64.09371388,148.46,4,9,12.4
```

Query parameters:

| Name | Type | Description | Example | Required | Default |
| - | - | - | - | - | - |
| `data_format` | String | The format of the HTTP response body data. | *json* or *csv*| No | *json* |

Errors:

| HTTP code | Description |
| - | - |
| 400 | The requested `data_format` is not supported. |

## 2 Ingestion - Storing new data

Endpoint:
```
POST /api/ingest
```

Requests to the ingestion endpoint will receive `record` objects in the same form that the retrieval enpoint responds with.

The `record` object is sent within the body of the HTTP POST request.

### 2.1 Authentication

Before sending data, you must register an API key in the glacsweb database. This must be done manually by adding an entry to the api_keys table in the Glacsweb database. The API key must be an alphanumeric string.

Once obtained, this key should be included in the request body, under the attribute "api_key".

An example request body:
```
{
    "api_key": "foobarbaz",
    "records": [
        ...
    ]
}
```
Authentication can fail with the following errors:

| HTTP code | Description |
| - | - |
| 400 | The request body contains no `api_key` key. |
| 400 | The API key is not registered. |

#### 2.2 Request body encoding formats

The request body format is specified by the `Content-Type` HTTP header value, and will be one of the following:

| Data format | Content-Type (MIME type) |
| - | - |
| JSON | application/json |
| CBOR | application/cbor |

If no `Content-Type`, or an invalid `Content-Type` is supplied, then the API assumes the body is in JSON format.

#### 2.3 Request body errors

All ingest requests should contain a HTTP request body. If this request body is missing or malformed, then you may receive the following error responses from the API:

| HTTP code | Description |
| - | - |
| 400 | The request has no body. |
| 400 | The request body is badly formatted. |
| 400 | The request body contains no `records` key. |

### 2.4 JSON body

Full example request in JSON:

```
POST /api/ingest
HTTP/1.1
Host: <hostname>:<port>
Content-Type: application/json
Content-Length: 218

{
    "api_key": {{API key}},
    "records": [
        {
            "rover_id": 3,
            "timestamp": "2022-05-01 00:01:00",
            "longitude": -16.33418463,
            "latitude": 64.0937139,
            "altitude": 148.45,
            "quality": 4,
            "hdop": 1.0,
            "sats": 9,
            "temperature": 11.8
        }
    ]
}
```

### 2.5 CBOR body

To reduce the amount of data sent over the Glacsweb network, CBOR is also an data format option for ingestion.

Example request in CBOR:

```
POST /api/ingest
HTTP/1.1
Host: <hostname>:<port>
Content-Type: application/cbor
Content-Length: 128

b'\xa2gapi_keygtestkeygrecords\x81\xa6hrover_id\x03itimestamps2022-05-01 00:01:00ilongitude\xfb\xc00U\x8d\x1f\xb8\xad\x05hlatitude\xfb@P\x05\xffh\x95\xeb\x8fhaltitude\xfb@b\x8efffffdsats\t'
```

Note that the `Content-Length` is shorter compared to JSON for the same data, due to its more compact serialization.

### 2.6 Ingested fields

Note that the order of the fields within the `record` is irrelvant.

If some fields are not recorded, they do not need to be included e.g. `temperature`, `quality` or `hdop`.

The only *strictly* required fields are:
| Field name |
| - |
| rover_id |
| timestamp |
| longitude |
| latitude |
| altitude |
| sats |

### 2.7 Multi-record ingestion

Multiple records may be ingested in a single request by adding more objects in the JSON array, as shown below:

```
POST /api/ingest
HTTP/1.1
Host: <hostname>:<port>
Content-Type: application/json
Content-Length: 402

{
    "api_key": {{API key}},
    "records": [
        {
            "rover_id": 3,
            "timestamp": "2022-05-01 00:01:00",
            "longitude": -16.33418463,
            "latitude": 64.0937139,
            "altitude": 148.45,
            "quality": 4,
            "hdop": 1.0,
            "sats": 9,
            "temperature": 11.8
        },
            ...
        {
            "rover_id": 3,
            "timestamp": "2022-05-03 08:01:00",
            "longitude": -16.34508123,
            "latitude": 64.11240578,
            "altitude": 148.23,
            "quality": 4,
            "hdop": 1.0,
            "sats": 9,
            "temperature": 11.7
        }
    ]
}
```

### 2.8 Ingestion responses

If the ingestion request body is formatted correctly, then a response will be returned with HTTP code 200.

Each record is checked against validation criteria to ensure that the values *can* be inserted into the database. For each of the records ingested, the response will contain lines corresponding to the outcome of ingesting this record.

Note: There may be multiple outcome lines for an invalid record - each line corresponding to a different failed validation check.

Responses are in the form:

```
Received n records.

Valid: a
Duplicated: b
Invalid: c

A list of outcomes after attempting to ingest each record...
```

An example response body:
```
Received 4 records.

Valid: 2
Duplicated: 2
Invalid: 1

Record 0 valid.
Record 1 valid.
Record 2 invalid: The required field 'rover_id' has not been included in the record.
Record 2 invalid: The timestamp is not a valid datetime.
Record 3 duplicated.
```

Possible ingestion outcomes for each record:

| Response line |
| - |
| Record *n* valid. |
| Record *n* duplicated. |
| Record *n* invalid: The requested field '`{{field name}}`' does not exist. |
| Record *n* invalid: The `{{field name}}` is required. |
| Record *n* invalid: The `rover_id` is not a valid integer. |
| Record *n* invalid: The `rover_id` is not registered to an existing rover. |
| Record *n* invalid: The `timestamp` is not a valid datetime. |
| Record *n* invalid: The `longitude` is not a valid double. |
| Record *n* invalid: The `latitude` is not a valid double. |
| Record *n* invalid: The `altitude` is not a valid double. |
| Record *n* invalid: The `quality` is not a valid integer. |
| Record *n* invalid: The `hdop` is not a valid double. |
| Record *n* invalid: The `sats` is not a valid integer. |
| Record *n* invalid: The `temperature` is not a valid double. |

## 3 Querying additional information

### 3.1 Rover IDs list

This endpoint returns a list of registered IDs and glaciers for each rover.

Endpoint:
```
GET /api/query/rovers
```

Example request:
```
GET /api/query/rovers
?hide_unused
HTTP/1.1
Host: <hostname>:<port>
```

Example response:

```json
[
    {
        "rover_id": 1,
        "glacier": "Fjallsjokull Position 1"
    },
       ...
    {
        "rover_id": 13,
        "glacier": "Breidamerkurjokull Position 3"
    },

]
```

Query parameters:

| Name | Type | Description | Example | Required |
| - | - | - | - | - |
| `hide_unused` | None | Determines if we should include rovers with no associated records in the output (aka unused rovers). | \*Dictated by presence of parameter | No |

### 3.2 Rover timestamp range

These endpoints return the upper and lower bounds of timestamps for records belonging to a specific `rover_id`

#### 3.2.1 Getting the first recorded timestamp

Endpoint:

```
GET /api/query/timestamp_min
```

Example request:
```
GET /api/query/timestamp_min
?rover_id={{rover id}}
HTTP/1.1
Host: <hostname>:<port>
```

Example response:

```json
{
    "timestamp": "2019-08-31T12:10:00"
}
```

#### 3.2.2 Getting the last recorded timestamp

Endpoint:

```
GET /api/query/timestamp_max
```

Example request:
```
GET /api/query/timestamp_max
?rover_id={{rover id}}
HTTP/1.1
Host: <hostname>:<port>
```

Example response:

```json
{
    "timestamp": "2022-09-28T15:10:00"
}
```

#### 3.2.3 Query parameters for timestamp range queries

| Name | Type | Description | Example | Required |
| - | - | - | - | - |
| `rover_id` | Integer | The unique identifier for the rover device from which readings are required from. | *4* | Yes |

#### 3.2.4 Possible errors for timestamp range queries

| HTTP code | Description |
| - | - |
| 400 | The `rover_id` is required. |
| 400 | The `rover_id` is not a valid integer. |
| 400 | The `rover_id` is not registered to an existing rover. |
| 400 | The `rover_id` has no existing data records associated with it. |