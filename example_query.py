import requests

API_URL = "http://127.0.0.1:8001/query"

payload = {
    "user_id": "example_user_1",
    "query": "What is the battery life of the Outdoor Speaker?"
}

response = requests.post(API_URL, json=payload)

if response.status_code == 200:
    data = response.json()
    print(" Query:", data["query"])
    print(" Answer:", data["answer"])
    print(" Documents:", [doc["page_content"] for doc in data.get("docs", [])])
    print(" History:")
    for msg in data.get("history", []):
        print(f"  - [{msg['type']}] {msg['content']}")
else:
    print(" Request failed with status code:", response.status_code)
    print(response.text)
