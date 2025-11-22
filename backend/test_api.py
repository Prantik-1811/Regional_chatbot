import requests
import json

try:
    response = requests.post(
        "http://localhost:8000/query",
        json={"query": "cybersecurity"}
    )
    print(response.json())
except Exception as e:
    print(e)
