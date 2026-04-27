import requests
import os

QUMRA_API_URL = os.getenv("QUMRA_API_URL")
QUMRA_TOKEN = os.getenv("QUMRA_API_KEY")

def query_qumra(query, variables=None):
    headers = {
        "Authorization": f"Bearer {QUMRA_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {"query": query, "variables": variables}
    try:
        response = requests.post(QUMRA_API_URL, json=payload, headers=headers)
        return response.json()
    except Exception as e:
        print(f"🔴 خطأ في اتصال قمرة: {e}")
        return None
