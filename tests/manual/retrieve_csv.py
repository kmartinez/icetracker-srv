import requests
    
response = requests.get(
    url="http://localhost:5000/api/retrieve",
    params={
        "timestamp_start": "2017-09-01T00:00",
        "timestamp_end":   "2017-09-02T00:00",
        "data_format":     "csv"
    }
)

print(response.text)