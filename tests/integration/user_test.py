from tests.factories import user_payload, create_contract_using_api
from models.user import User
from app import db
import uuid


def test_users_first_success(client):
    """Test creating the first user in the system"""
    payload = {
        "email": "firstuser@example.com",
        "password": "SecurePass123",
        "full_name": "First User",
        "role": "admin"
    }
    
    res = client.post("/users-first", json=payload)
    assert res.status_code == 201
    assert "user_id" in res.get_json()["data"]


def test_users_first_invalid_role(client):
    """Test creating first user with invalid role"""
    payload = {
        "email": "firstuser@example.com",
        "password": "SecurePass123",
        "full_name": "First User",
        "role": "superadmin"
    }
    
    res = client.post("/users-first", json=payload)
    assert res.status_code == 400
    assert "Role must be 'employee' or 'admin'" in res.get_json()["message"]


def test_users_first_missing_field(client):
    """Test creating first user with missing required field"""
    payload = {
        "email": "firstuser@example.com",
        "password": "SecurePass123",
        "full_name": "First User",
         "role": None
    }
    
    res = client.post("/users-first", json=payload)
    assert res.status_code == 400
    assert "Missing required fields" in res.get_json()["message"]


def test_users_first_null_field(client):
    """Test creating first user with null required field"""
    payload = {
        "email": None,
        "password": "SecurePass123",
        "full_name": "First User",
        "role": "admin"
    }
    
    res = client.post("/users-first", json=payload)
    assert res.status_code == 400
    assert "Missing required fields" in res.get_json()["message"]


def test_users_first_db_error(client, monkeypatch):
    """Test users-first exception when database commit fails"""
    def mock_commit():
        raise Exception("Database connection error")
    
    monkeypatch.setattr("app.db.session.commit", mock_commit)
    
    payload = {
        "email": "firstuser@example.com",
        "password": "SecurePass123",
        "full_name": "First User",
        "role": "admin"
    }
    
    res = client.post("/users-first", json=payload)
    assert res.status_code == 400
    assert "Error creating first user" in res.get_json()["message"]



def test_create_user_success(client, auth_headers):
    """Test creating a user with valid credentials as admin"""
    payload = user_payload()
    res = client.post("/users", headers=auth_headers, json=payload)

    assert res.status_code == 201
    assert res.get_json()["message"] == "User created successfully"
    created_user = res.get_json()["data"]["user"]
    assert created_user["email"] == payload["email"]
    assert created_user["full_name"] == payload["full_name"]


def test_create_user_non_admin(client, app, monkeypatch):
    """Test that non-admin users cannot create users"""
    import uuid as uuid_module
    from flask_jwt_extended import create_access_token
    
    with app.app_context():
        user = User(email="employee@example.com", full_name="Employee", role="employee")
        user.set_password("pass12345")
        db.session.add(user)
        db.session.commit()
        user_id = user.id
        
        token = create_access_token(identity=str(user_id))
        uuid_identity = uuid_module.UUID(str(user_id))
    
    monkeypatch.setattr("blueprints.user.get_jwt_identity", lambda: uuid_identity)
    
    payload = user_payload()
    res = client.post("/users", headers={"Authorization": f"Bearer {token}"}, json=payload)
    
    assert res.status_code == 400
    assert "Only admin users can create new users" in res.get_json()["message"]


def test_create_user_validation_error(client, auth_headers):
    """Test creating user with invalid data (validation error)"""
    payload = {
        "email": "invalid-email",
        "full_name": "Test User",
        "password": "SecurePass123",
        "role": "employee"
    }
    res = client.post("/users", headers=auth_headers, json=payload)
    assert res.status_code == 400
    assert "Validation error" in res.get_json()["message"]


def test_create_user_duplicate_email(client, auth_headers):
    """Test creating user with duplicate email"""
    payload = user_payload(email="duplicate@example.com")
    
    client.post("/users", headers=auth_headers, json=payload)
    res = client.post("/users", headers=auth_headers, json=payload)
    
    assert res.status_code == 400
    assert "Validation error" in res.get_json()["message"]


def test_create_user_db_error(client, auth_headers, monkeypatch):
    """Test create user exception when database commit fails"""
    def mock_commit():
        raise Exception("Database connection error")
    
    monkeypatch.setattr("app.db.session.commit", mock_commit)
    
    payload = user_payload()
    res = client.post("/users", headers=auth_headers, json=payload)
    
    assert res.status_code == 400
    assert "Error creating user" in res.get_json()["message"]


# ===== USERS ENDPOINT (GET - List) =====

def test_get_users_success(client, auth_headers):
    """Test getting all users"""
    payload = user_payload()
    client.post("/users", headers=auth_headers, json=payload)

    res = client.get("/users", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()["message"] == "Users retrieved successfully"
    users = res.get_json()["data"]["users"]
    assert len(users) >= 1


def test_get_users_excludes_archived(client, auth_headers):
    """Test that archived users are not included in list"""
    payload = user_payload()
    res_post = client.post("/users", headers=auth_headers, json=payload)
    user_id = res_post.get_json()["data"]["user"]["id"]
    
    client.delete(f"/users/{user_id}", headers=auth_headers)
    
    res = client.get("/users", headers=auth_headers)
    users = res.get_json()["data"]["users"]
    user_ids = [u["id"] for u in users]
    
    assert user_id not in user_ids


def test_get_users_db_error(client, auth_headers, monkeypatch):
    """Test get users exception when database query fails"""
    def mock_filter(*args, **kwargs):
        raise Exception("Database query error")
    
    from blueprints.user import User
    
    class MockQuery:
        def filter_by(self, **kwargs):
            raise Exception("Database query error")
    
    monkeypatch.setattr("blueprints.user.User.query", MockQuery())
    
    res = client.get("/users", headers=auth_headers)
    assert res.status_code == 400
    assert "Error retrieving users" in res.get_json()["message"]



def test_get_user_by_id_success(client, auth_headers): 
    """Test getting a user by ID"""
    payload = user_payload()
    res_post = client.post("/users", headers=auth_headers, json=payload)
    user_id = res_post.get_json()["data"]["user"]["id"]

    res = client.get(f"/users/{user_id}", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()["message"] == "User retrieved successfully"
    fetched_user = res.get_json()["data"]["user"]
    assert fetched_user["id"] == user_id
    assert fetched_user["email"] == payload["email"]


def test_get_user_by_id_not_found(client, auth_headers):
    """Test getting non-existent user"""
    non_existent_id = str(uuid.uuid4())
    res = client.get(f"/users/{non_existent_id}", headers=auth_headers)
    assert res.status_code == 404
    assert res.get_json()["message"] == "User not found"


def test_get_user_by_id_archived(client, auth_headers):
    """Test that archived users cannot be retrieved"""
    payload = user_payload()
    res_post = client.post("/users", headers=auth_headers, json=payload)
    user_id = res_post.get_json()["data"]["user"]["id"]
    
    client.delete(f"/users/{user_id}", headers=auth_headers)
    
    res = client.get(f"/users/{user_id}", headers=auth_headers)
    assert res.status_code == 404


def test_get_user_by_id_invalid_uuid(client, auth_headers):
    """Test getting user with invalid UUID format"""
    res = client.get(f"/users/invalid-uuid", headers=auth_headers)
    assert res.status_code == 500
    assert "Error getting user" in res.get_json()["message"]


def test_get_user_by_id_db_error(client, auth_headers, monkeypatch):
    """Test get user exception when database query fails"""
    def mock_query(*args, **kwargs):
        raise Exception("Database query error")
    
    monkeypatch.setattr("blueprints.user.db.session.query", mock_query)
    
    user_id = str(uuid.uuid4())
    res = client.get(f"/users/{user_id}", headers=auth_headers)
    
    assert res.status_code == 500
    assert "Error getting user" in res.get_json()["message"]



def test_update_patch_user_success(client, auth_headers):
    """Test partial update of user"""
    payload = user_payload()
    res_post = client.post("/users", headers=auth_headers, json=payload)
    user_id = res_post.get_json()["data"]["user"]["id"]

    update_payload = {"full_name": "Updated Name"}

    res = client.patch(f"/users/{user_id}", headers=auth_headers, json=update_payload)
    assert res.status_code == 200
    assert res.get_json()["data"]["user"]["full_name"] == "Updated Name"


def test_update_put_user_success(client, auth_headers):
    """Test full update of user"""
    payload = user_payload()
    res_post = client.post("/users", headers=auth_headers, json=payload)
    user_id = res_post.get_json()["data"]["user"]["id"]

    update_payload = {
        "full_name": "Updated Name",
        "email": "updatedemail@example.com",
        "password": "NewSecurePass123",
        "role": "employee"
    }

    res = client.put(f"/users/{user_id}", headers=auth_headers, json=update_payload)
    assert res.status_code == 200
    updated_user = res.get_json()["data"]["user"]
    assert updated_user["full_name"] == "Updated Name"
    assert updated_user["email"] == "updatedemail@example.com"


def test_update_user_not_found(client, auth_headers):
    """Test updating non-existent user"""
    non_existent_id = str(uuid.uuid4())
    update_payload = {"full_name": "New Name"}
    
    res = client.patch(f"/users/{non_existent_id}", headers=auth_headers, json=update_payload)
    assert res.status_code == 404


    



def test_update_user_validation_error(client, auth_headers):
    """Test updating user with invalid data"""
    payload = user_payload()
    res_post = client.post("/users", headers=auth_headers, json=payload)
    user_id = res_post.get_json()["data"]["user"]["id"]

    update_payload = {"email": "invalid-email"}
    res = client.patch(f"/users/{user_id}", headers=auth_headers, json=update_payload)
    assert res.status_code == 400
    assert "Validation error" in res.get_json()["message"]


def test_update_user_duplicate_email(client, auth_headers):
    """Test updating user with duplicate email"""
    payload1 = user_payload(email="user1@example.com")
    payload2 = user_payload(email="user2@example.com")
    
    res_post1 = client.post("/users", headers=auth_headers, json=payload1)
    res_post2 = client.post("/users", headers=auth_headers, json=payload2)
    
    user_id2 = res_post2.get_json()["data"]["user"]["id"]

    update_payload = {"email": "user1@example.com"}
    res = client.patch(f"/users/{user_id2}", headers=auth_headers, json=update_payload)
    
    assert res.status_code == 400


def test_update_user_db_error(client, auth_headers, monkeypatch):
    """Test update user exception when database commit fails"""
    payload = user_payload()
    res_post = client.post("/users", headers=auth_headers, json=payload)
    user_id = res_post.get_json()["data"]["user"]["id"]
    
    def mock_commit():
        raise Exception("Database connection error")
    
    monkeypatch.setattr("app.db.session.commit", mock_commit)
    
    update_payload = {"full_name": "Updated Name"}
    res = client.patch(f"/users/{user_id}", headers=auth_headers, json=update_payload)
    
    assert res.status_code == 500
    assert "Error updating user" in res.get_json()["message"]


def test_delete_user_success(client, auth_headers):
    """Test archiving a user"""
    payload = user_payload()
    res_post = client.post("/users", headers=auth_headers, json=payload)
    user_id = res_post.get_json()["data"]["user"]["id"]

    res = client.delete(f"/users/{user_id}", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()["message"] == "User archived successfully"
    assert res.get_json()["data"]["user"]["is_archived"] is True


def test_delete_user_not_found(client, auth_headers):
    """Test deleting non-existent user"""
    non_existent_id = str(uuid.uuid4())
    res = client.delete(f"/users/{non_existent_id}", headers=auth_headers)
    assert res.status_code == 404


def test_delete_user_db_error(client, auth_headers, monkeypatch):
    """Test delete user exception when database commit fails"""
    payload = user_payload()
    res_post = client.post("/users", headers=auth_headers, json=payload)
    user_id = res_post.get_json()["data"]["user"]["id"]
    
    def mock_commit():
        raise Exception("Database connection error")
    
    monkeypatch.setattr("app.db.session.commit", mock_commit)
    
    res = client.delete(f"/users/{user_id}", headers=auth_headers)
    
    assert res.status_code == 500
    assert "Error archiving user" in res.get_json()["message"]


# ===== USER CONTRACTS ENDPOINT =====

def test_get_user_contracts_success(client, auth_headers):
    """Test getting contracts created by a user"""
    contract = create_contract_using_api(client, auth_headers)
    user_id = contract["created_by"]
    
    res = client.get(f"/users/{user_id}/contracts", headers=auth_headers)
    assert res.status_code == 200
    assert "contracts" in res.get_json()["data"]
    assert len(res.get_json()["data"]["contracts"]) >= 1


def test_get_user_contracts_empty(client, auth_headers):
    """Test getting contracts for user with no contracts"""
    payload = user_payload()
    res_post = client.post("/users", headers=auth_headers, json=payload)
    user_id = res_post.get_json()["data"]["user"]["id"]
    
    res = client.get(f"/users/{user_id}/contracts", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()["data"]["contracts"] == []


def test_get_user_contracts_not_found(client, auth_headers):
    """Test getting contracts for non-existent user"""
    non_existent_id = str(uuid.uuid4())
    res = client.get(f"/users/{non_existent_id}/contracts", headers=auth_headers)
    assert res.status_code == 404


def test_get_user_contracts_invalid_uuid(client, auth_headers):
    """Test get user contracts with invalid UUID format"""
    res = client.get(f"/users/invalid-uuid/contracts", headers=auth_headers)
    assert res.status_code == 500
    assert "Error getting contracts" in res.get_json()["message"]


def test_get_user_contracts_db_error(client, auth_headers, monkeypatch):
    """Test get user contracts exception when database query fails"""
    def mock_query(*args, **kwargs):
        raise Exception("Database query error")
    
    monkeypatch.setattr("blueprints.user.db.session.query", mock_query)
    
    user_id = str(uuid.uuid4())
    res = client.get(f"/users/{user_id}/contracts", headers=auth_headers)
    
    assert res.status_code == 404
    assert "User not found" in res.get_json()["message"]