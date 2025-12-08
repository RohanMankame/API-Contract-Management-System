# tests/factories.py
import uuid


def user_payload(**overrides):
    base = {
        "email": f"testuser-{uuid.uuid4().hex}@example.com",
        "full_name": "Test User",
        "password": "pass12345",
    }
    base.update(overrides)
    return base



def product_payload(**overrides):
    base = {
        "api_name": "Test API",
        "description": "This is a test API product.",
    }
    base.update(overrides)
    return base


def client_payload(**overrides):
    base = {
        "company_name": "Test Client",
        "email": f"testclient-{uuid.uuid4().hex}@example.com",
        "phone_number": "555-555-5555",
        "address": "123 Test St",
    }
    base.update(overrides)
    return base




def contract_payload(client_id, **overrides):
    base = {
        "client_id": client_id,
        "contract_name": "Test Contract",
    }
    base.update(overrides)
    return base


def subscription_payload(contract_id, product_id, **overrides):
    base = {
        "contract_id": contract_id,
        "product_id": product_id,
        "pricing_type": "Fixed",
        "strategy": "Fixed",
    }
    base.update(overrides)
    return base




def create_user_using_api(client, auth_headers, payload=None):
    payload = payload or user_payload()
    res = client.post("/Users", headers=auth_headers, json=payload)
    assert res.status_code == 201, f"create_user failed: {res.get_data(as_text=True)}"
    return res.get_json()["user"]

# create client
def create_client_using_api(client, auth_headers, payload=None):
    payload = payload or client_payload()
    res = client.post("/Clients", headers=auth_headers, json=payload)
    assert res.status_code == 201, f"create_client failed: {res.get_data(as_text=True)}"
    return res.get_json()["client"]

# create product
def create_product_using_api(client, auth_headers, payload=None):
    payload = payload or product_payload()
    res = client.post("/Products", headers=auth_headers, json=payload)
    assert res.status_code == 201, f"create_product failed: {res.get_data(as_text=True)}"
    return res.get_json()["product"]

# create contract
def create_contract_using_api(client, auth_headers, client_id=None, payload=None):
    if client_id is None:
        client_obj = create_client_using_api(client, auth_headers)
        client_id = client_obj["id"]
    payload = payload or contract_payload(client_id)
    res = client.post("/Contracts", headers=auth_headers, json=payload)
    assert res.status_code == 201, f"create_contract failed: {res.get_data(as_text=True)}"
    return res.get_json()["contract"]

# create product + client + contract 
def create_subscription_dependencies(client, auth_headers, client_payload=None, product_payload=None, contract_payload_overrides=None):
    product_obj = create_product_using_api(client, auth_headers, product_payload)
    client_obj = create_client_using_api(client, auth_headers, client_payload)
    contract_obj = create_contract_using_api(client, auth_headers, client_obj["id"], payload=contract_payload_overrides)
    return {"product": product_obj, "client": client_obj, "contract": contract_obj}



