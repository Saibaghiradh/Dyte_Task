# send_log.py

import requests

log_data = {
    "level": "error",
    "message": "Failed to connect to DB",
    "resourceId": "server-1234",
    "timestamp": "2023-09-15T08:00:00Z",
    "traceId": "abc-xyz-123",
    "spanId": "span-456",
    "commit": "5e5342f",
    "metadata": {
        "parentResourceId": "server-0987"
    }
}

url = "http://localhost:3000/ingest"
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=log_data, headers=headers)

print(response.status_code)

try:
    print(response.json())
except ValueError:
    print(response.text)
