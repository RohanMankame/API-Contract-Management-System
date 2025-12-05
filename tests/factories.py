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