import requests
import json

request_body = {
    "api_key": "testkey",
    "records": [{
        "rover_id": 3,
        "timestamp": "2022-05-01 00:01:00",
        "longitude": -16.33418463,
        "latitude": 64.0937139,
        "altitude": 148.45,
        "sats": 9
    }]
}

json_request_body = json.dumps(request_body)
    
requests.post(
    url="http://localhost/api/ingest",
    data=json_request_body,
    headers={"Content-Type":"application/json"}
)