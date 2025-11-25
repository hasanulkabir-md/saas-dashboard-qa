import requests

BASE = "http://localhost:8000"

def test_create_user():
    payload = {"name": "Kabir", "email": "kabir@example.com"}
    r = requests.post(f"{BASE}/user/create", json=payload)
    assert r.status_code == 200

def test_list_users():
    r = requests.get(f"{BASE}/user/list")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
