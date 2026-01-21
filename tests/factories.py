# tests/factories.py
import uuid


def user_payload(**overrides):
    base = {
        "email": f"testuser-{uuid.uuid4().hex}@example.com",
        "full_name": "Test User",
        "password": "pass12345",
        "role": "employee",
    }
    base.update(overrides)
    return base


def product_payload(**overrides):
    base = {
        "api_name": f"Test API {uuid.uuid4().hex[:8]}",
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


def invalid_client_payload(**overrides):
    base = {
        "company_name": "Test Client",
        "email": "invalid-email-format",
        "phone_number": "555-555-5555",
        "address": "123 Test St",
    }
    base.update(overrides)
    return base


def contract_payload(client_id, **overrides):
    base = {
        "client_id": client_id,
        "contract_name": "Test Contract",
        "start_date": "2025-01-01T00:00:00.000Z",
        "end_date": "2026-12-31T23:59:59.999Z",
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


def rate_card_payload(subscription_id, **overrides):
    """Factory for creating rate card payloads"""
    base = {
        "subscription_id": subscription_id,
        "start_date": "2025-12-08T09:25:18.505Z",
        "end_date": "2027-11-08T09:25:18.505Z",
    }
    base.update(overrides)
    return base


def subscription_tier_payload(rate_card_id, **overrides):
    """Factory for creating subscription tier payloads - now links to rate_card, not subscription"""
    base = {
        "rate_card_id": rate_card_id,
        "min_calls": 0,
        "max_calls": 1000,
        "unit_price": 10.00,
    }
    base.update(overrides)
    return base


# --- API Helper Functions ---

def create_user_using_api(client, auth_headers, payload=None):
    payload = payload or user_payload()
    res = client.post("/users", headers=auth_headers, json=payload)
    assert res.status_code == 201, f"create_user failed: {res.get_data(as_text=True)}"
    return res.get_json()["data"]["user"]


def create_client_using_api(client, auth_headers, payload=None):
    payload = payload or client_payload()
    res = client.post("/clients", headers=auth_headers, json=payload)
    assert res.status_code == 201, f"create_client failed: {res.get_data(as_text=True)}"
    return res.get_json()["data"]["client"]


def create_product_using_api(client, auth_headers, payload=None):
    payload = payload or product_payload()
    res = client.post("/products", headers=auth_headers, json=payload)
    assert res.status_code == 201, f"create_product failed: {res.get_data(as_text=True)}"
    return res.get_json()["data"]["product"]


def create_contract_using_api(client, auth_headers, client_id=None, payload=None):
    if client_id is None:
        client_obj = create_client_using_api(client, auth_headers)
        client_id = client_obj["id"]
    payload = payload or contract_payload(client_id)
    res = client.post("/contracts", headers=auth_headers, json=payload)
    assert res.status_code == 201, f"create_contract failed: {res.get_data(as_text=True)}"
    return res.get_json()["data"]["contract"]


def create_subscription_dependencies(client, auth_headers, client_payload_arg=None, product_payload_arg=None, contract_payload_overrides=None):
    """Create product, client, and contract for subscription tests"""
    product_obj = create_product_using_api(client, auth_headers, product_payload_arg)
    client_obj = create_client_using_api(client, auth_headers, client_payload_arg)
    contract_obj = create_contract_using_api(client, auth_headers, client_obj["id"], payload=contract_payload_overrides)
    return {"product": product_obj, "client": client_obj, "contract": contract_obj}


def create_subscription_using_api(client, auth_headers, contract_id, product_id, payload=None):
    payload = payload or subscription_payload(contract_id, product_id)
    res = client.post("/subscriptions", headers=auth_headers, json=payload)
    assert res.status_code == 201, f"create_subscription failed: {res.get_data(as_text=True)}"
    return res.get_json()["data"]["subscription"]


def create_rate_card_using_api(client, auth_headers, subscription_id, payload=None):
    """Create a rate card for a subscription"""
    payload = payload or rate_card_payload(subscription_id)
    res = client.post("/rate-cards", headers=auth_headers, json=payload)
    assert res.status_code == 201, f"create_rate_card failed: {res.get_data(as_text=True)}"
    return res.get_json()["data"]["rate_card"]


def create_subscription_tier_using_api(client, auth_headers, rate_card_id, payload=None):
    """Create a subscription tier for a rate card"""
    payload = payload or subscription_tier_payload(rate_card_id)
    res = client.post("/subscription-tiers", headers=auth_headers, json=payload)
    assert res.status_code == 201, f"create_subscription_tier failed: {res.get_data(as_text=True)}"
    return res.get_json()["data"]["subscription_tier"]