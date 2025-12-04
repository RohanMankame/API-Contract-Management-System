# tests/factories.py
import uuid

def client_payload(**overrides):
    base = {
        "company_name": "Test Client",
        "email": f"testclient-{uuid.uuid4().hex}@example.com",
        "phone_number": "555-555-5555",
        "address": "123 Test St",
    }
    base.update(overrides)
    return base

def create_client_using_api(client, auth_headers, payload=None):
    payload = payload or client_payload()
    resp = client.post("/Clients", headers=auth_headers, json=payload)
    assert resp.status_code == 201, f"create_client failed: {resp.get_data(as_text=True)}"
    return resp.get_json()["client"]