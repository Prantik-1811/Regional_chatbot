import requests
import json

try:
    response = requests.post(
        "http://localhost:8000/query",
        json={"query": "What is ransomware?", "region": "HK"}
    )
    print("Status Code:", response.status_code)
    print("\nResponse JSON:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print("Error:", e)
