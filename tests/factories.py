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
        "pricing_type": "fixed",
        "strategy": "standard",
    }
    base.update(overrides)
    return base