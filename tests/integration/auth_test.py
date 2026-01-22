# tests/integration/auth_test.py
from tests.factories import user_payload
from models.user import User
from app import db
import uuid
import json


def test_login_success(client):
    """Test successful login with valid credentials"""
    user = User(email="testuser@example.com", full_name="Test User", role="employee")
    user.set_password("testpass123")
    db.session.add(user)
    db.session.commit()
    
    res = client.post("/login", json={
        "email": "testuser@example.com",
        "password": "testpass123"
    })
    
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "token" in data["data"]
    assert isinstance(data["data"]["token"], str)
    assert data["message"] == "Login successful"


def test_login_invalid_email(client):
    """Test login with non-existent email"""
    res = client.post("/login", json={
        "email": "nonexistent@example.com",
        "password": "anypassword"
    })
    
    assert res.status_code == 400
    data = res.get_json()
    assert data["success"] is False
    assert "Invalid credentials" in data["message"]


def test_login_incorrect_password(client):
    """Test login with incorrect password"""
    # Create a user first
    user = User(email="testuser@example.com", full_name="Test User", role="employee")
    user.set_password("correctpassword")
    db.session.add(user)
    db.session.commit()
    
    res = client.post("/login", json={
        "email": "testuser@example.com",
        "password": "wrongpassword"
    })
    
    assert res.status_code == 400
    data = res.get_json()
    assert data["success"] is False
    assert "Invalid credentials" in data["message"]


def test_login_missing_email(client):
    """Test login with missing email"""
    res = client.post("/login", json={
        "password": "somepassword"
    })
    
    assert res.status_code == 400
    data = res.get_json()
    assert data["success"] is False
    assert "Email and password are required" in data["message"]


def test_login_missing_password(client):
    """Test login with missing password"""
    res = client.post("/login", json={
        "email": "testuser@example.com"
    })
    
    assert res.status_code == 400
    data = res.get_json()
    assert data["success"] is False
    assert "Email and password are required" in data["message"]



def test_login_null_email(client):
    """Test login with null email"""
    res = client.post("/login", json={
        "email": None,
        "password": "somepassword"
    })
    
    assert res.status_code == 400
    data = res.get_json()
    assert data["success"] is False
    assert "Email and password are required" in data["message"]


def test_login_null_password(client):
    """Test login with null password"""
    res = client.post("/login", json={
        "email": "testuser@example.com",
        "password": None
    })
    
    assert res.status_code == 400
    data = res.get_json()
    assert data["success"] is False
    assert "Email and password are required" in data["message"]


def test_login_empty_body(client):
    """Test login with empty request body"""
    res = client.post("/login", json={})
    
    assert res.status_code == 400
    data = res.get_json()
    assert data["success"] is False
    assert "Invalid request body" in data["message"]


def test_login_empty_string_email(client):
    """Test login with empty string email"""
    res = client.post("/login", json={
        "email": "",
        "password": "somepassword"
    })
    
    assert res.status_code == 400
    data = res.get_json()
    assert data["success"] is False
    assert "Email and password are required" in data["message"]


def test_login_empty_string_password(client):
    """Test login with empty string password"""
    res = client.post("/login", json={
        "email": "testuser@example.com",
        "password": ""
    })
    
    assert res.status_code == 400
    data = res.get_json()
    assert data["success"] is False
    assert "Email and password are required" in data["message"]


def test_login_Exception_error(client):
    """Test login with empty string password"""
    res = client.post("/login", json=None)
    
    assert res.status_code == 500
    data = res.get_json()
    assert data["success"] is False
    assert "An error occurred during login" in data["message"]


def test_login_case_sensitive_email(client):
    """Test login with different case email"""
    # Create a user with lowercase email
    user = User(email="testuser@example.com", full_name="Test User", role="employee")
    user.set_password("testpass123")
    db.session.add(user)
    db.session.commit()
    
    # Try logging in with uppercase
    res = client.post("/login", json={
        "email": "TESTUSER@EXAMPLE.COM",
        "password": "testpass123"
    })
    
    assert res.status_code == 400
    data = res.get_json()
    assert "Invalid credentials" in data["message"]


def test_login_whitespace_password(client):
    """Test login with whitespace-only password"""
    user = User(email="testuser@example.com", full_name="Test User", role="employee")
    user.set_password("correctpassword")
    db.session.add(user)
    db.session.commit()
    
    res = client.post("/login", json={
        "email": "testuser@example.com",
        "password": "   "
    })
    
    assert res.status_code == 400
    data = res.get_json()
    assert "Invalid credentials" in data["message"]


def test_login_returns_valid_jwt_format(client):
    """Test that login returns a valid JWT token format"""
    user = User(email="testuser@example.com", full_name="Test User", role="employee")
    user.set_password("testpass123")
    db.session.add(user)
    db.session.commit()
    
    res = client.post("/login", json={
        "email": "testuser@example.com",
        "password": "testpass123"
    })
    
    assert res.status_code == 200
    token = res.get_json()["data"]["token"]
    # JWT tokens have 3 parts separated by dots
    assert token.count(".") == 2



def test_protected_endpoint_with_valid_token(client, saved_token):
    """Test accessing protected endpoint with valid JWT token"""
    res = client.get("/protected", headers={"Authorization": f"Bearer {saved_token}"})
    
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "email" in data["data"]
    assert data["message"] == "Protected endpoint accessed successfully"


def test_protected_endpoint_no_token(client):
    """Test accessing protected endpoint without token"""
    res = client.get("/protected")
    
    assert res.status_code == 401


def test_protected_endpoint_invalid_token_format(client):
    """Test accessing protected endpoint with invalid token format"""
    res = client.get("/protected", headers={"Authorization": "Bearer invalid-token"})
    
    assert res.status_code == 422


def test_protected_endpoint_malformed_header(client):
    """Test accessing protected endpoint with malformed auth header"""
    res = client.get("/protected", headers={"Authorization": "InvalidTokenFormat"})
    
    assert res.status_code == 401


def test_protected_endpoint_empty_token(client):
    """Test protected endpoint handling unexpected exception"""
    res = client.get("/protected", headers={"Authorization": "Bearer "})
    
    assert res.status_code == 422



def test_protected_endpoint_schema_dump_error(client, saved_token, monkeypatch):
    """Test protected endpoint when schema dump raises an exception"""
    from schemas.user_schema import user_read_schema
    
    # Mock the dump method to raise an exception
    def mock_dump(obj):
        raise Exception("Schema dump failed")
    
    monkeypatch.setattr(user_read_schema, "dump", mock_dump)
    
    res = client.get("/protected", headers={"Authorization": f"Bearer {saved_token}"})
    
    assert res.status_code == 500
    data = res.get_json()
    assert data["success"] is False
    assert "An error occurred while fetching user data" in data["message"]

def test_protected_endpoint_returns_user_data(client, saved_token):
    """Test that protected endpoint returns correct user data"""
    res = client.get("/protected", headers={"Authorization": f"Bearer {saved_token}"})
    
    assert res.status_code == 200
    data = res.get_json()
    assert "email" in data["data"]
    assert "full_name" in data["data"]
    assert "role" in data["data"]
    assert "id" in data["data"]


def test_protected_endpoint_different_user_tokens(client, app):
    """Test protected endpoint with tokens from different users"""
    from flask_jwt_extended import create_access_token
    
    with app.app_context():
        # Create two users
        user1 = User(email=f"user1-{uuid.uuid4().hex}@example.com", full_name="User One", role="employee")
        user1.set_password("pass123")
        db.session.add(user1)
        db.session.commit()
        
        user2 = User(email=f"user2-{uuid.uuid4().hex}@example.com", full_name="User Two", role="admin")
        user2.set_password("pass123")
        db.session.add(user2)
        db.session.commit()
        
        token1 = create_access_token(identity=str(user1.id))
        token2 = create_access_token(identity=str(user2.id))
    
    # Test with user1 token
    res1 = client.get("/protected", headers={"Authorization": f"Bearer {token1}"})
    assert res1.status_code == 200
    
    # Test with user2 token
    res2 = client.get("/protected", headers={"Authorization": f"Bearer {token2}"})
    assert res2.status_code == 200


def test_login_then_access_protected(client):
    """Integration test: login then access protected endpoint"""
    # Create a user
    user = User(email="integrationtest@example.com", full_name="Integration User", role="employee")
    user.set_password("integrationpass123")
    db.session.add(user)
    db.session.commit()
    
    # Login
    login_res = client.post("/login", json={
        "email": "integrationtest@example.com",
        "password": "integrationpass123"
    })
    assert login_res.status_code == 200
    token = login_res.get_json()["data"]["token"]
    
    # Access protected endpoint with obtained token
    protected_res = client.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert protected_res.status_code == 200
    protected_data = protected_res.get_json()
    assert protected_data["data"]["email"] == "integrationtest@example.com"


def test_protected_endpoint_with_bearer_case_variations(client, saved_token):
    """Test protected endpoint with different cases of Bearer prefix"""
    # Standard "Bearer"
    res1 = client.get("/protected", headers={"Authorization": f"Bearer {saved_token}"})
    assert res1.status_code == 200
    
    # lowercase "bearer" - fails
    res2 = client.get("/protected", headers={"Authorization": f"bearer {saved_token}"})
    assert res2.status_code == 401


def test_protected_endpoint_with_deleted_user(client, app):
    """Test protected endpoint when user is deleted after login"""
    from flask_jwt_extended import create_access_token
    
    with app.app_context():
        # Create a user
        user = User(email=f"tempuser-{uuid.uuid4().hex}@example.com", full_name="Temp User", role="employee")
        user.set_password("pass123")
        db.session.add(user)
        db.session.commit()
        user_id = user.id
        
        # Create token
        token = create_access_token(identity=str(user_id))
        
        # Delete the user
        db.session.delete(user)
        db.session.commit()
    
    # Try accessing protected endpoint with deleted user's token
    res = client.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 404
    assert "User not found" in res.get_json()["message"]


def test_login_response_structure(client):
    """Test that login response has correct structure"""
    user = User(email="testuser@example.com", full_name="Test User", role="employee")
    user.set_password("testpass123")
    db.session.add(user)
    db.session.commit()
    
    res = client.post("/login", json={
        "email": "testuser@example.com",
        "password": "testpass123"
    })
    
    data = res.get_json()
    assert "success" in data
    assert "message" in data
    assert "data" in data
    assert "token" in data["data"]


def test_protected_response_structure(client, saved_token):
    """Test that protected endpoint response has correct structure"""
    res = client.get("/protected", headers={"Authorization": f"Bearer {saved_token}"})
    
    data = res.get_json()
    assert "success" in data
    assert "message" in data
    assert "data" in data


def test_login_multiple_times_different_tokens(client):
    """Test that multiple logins generate different tokens"""
    user = User(email="testuser@example.com", full_name="Test User", role="employee")
    user.set_password("testpass123")
    db.session.add(user)
    db.session.commit()
    
    res1 = client.post("/login", json={
        "email": "testuser@example.com",
        "password": "testpass123"
    })
    token1 = res1.get_json()["data"]["token"]
    
    res2 = client.post("/login", json={
        "email": "testuser@example.com",
        "password": "testpass123"
    })
    token2 = res2.get_json()["data"]["token"]
    
    # Tokens should be different due to JWT timestamps
    assert token1 != token2


def test_login_with_extra_fields(client):
    """Test login with extra fields in request body"""
    user = User(email="testuser@example.com", full_name="Test User", role="employee")
    user.set_password("testpass123")
    db.session.add(user)
    db.session.commit()
    
    res = client.post("/login", json={
        "email": "testuser@example.com",
        "password": "testpass123",
        "extra_field": "should_be_ignored"
    })
    
    assert res.status_code == 200
    assert "token" in res.get_json()["data"]


def test_protected_endpoint_with_extra_headers(client, saved_token):
    """Test protected endpoint with extra headers"""
    res = client.get("/protected", 
        headers={
            "Authorization": f"Bearer {saved_token}",
            "X-Custom-Header": "value"
        }
    )
    
    assert res.status_code == 200
