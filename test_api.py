import requests

BASE_URL = "http://127.0.0.1:5000"

def test_hello_api():
    res = requests.get(f"{BASE_URL}/hello")
    assert res.status_code == 200
    assert res.json()["message"] == "Hello, API!"
