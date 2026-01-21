from tests.factories import client_payload, invalid_client_payload
from uuid import uuid4

def test_create_client(client, auth_headers):
    payload = client_payload()
    res_post = client.post("/clients", headers=auth_headers, json=payload)
    assert res_post.status_code == 201
    assert res_post.get_json()["message"] == "Client created successfully"
    created_client = res_post.get_json()["data"]["client"]
    for key in payload:
        assert created_client[key] == payload[key]
    

def test_create_client_validation_error(client, auth_headers):
    payload = invalid_client_payload()
    res_post = client.post("/clients", headers=auth_headers, json=payload)
    assert res_post.status_code == 400
    assert res_post.get_json()["message"] == "Validation error"
    assert "email" in res_post.get_json()["errors"]
    assert "Invalid email address" in res_post.get_json()["errors"]["email"]


def test_create_client_missing_field(client, auth_headers):
    payload = client_payload()
    del payload["company_name"]
    res_post = client.post("/clients", headers=auth_headers, json=payload)
    assert res_post.status_code == 400
    assert res_post.get_json()["message"] == "Validation error"
    assert "company_name" in res_post.get_json()["errors"]


def test_create_client_missing_email(client, auth_headers):
    payload = client_payload()
    del payload["email"]
    res_post = client.post("/clients", headers=auth_headers, json=payload)
    assert res_post.status_code == 400
    assert res_post.get_json()["message"] == "Validation error"
    assert "email" in res_post.get_json()["errors"]


def test_create_client_testfail_validation(client, auth_headers):
    payload = client_payload()
    payload["company_name"] = "TestFailClient"
    res_post = client.post("/clients", headers=auth_headers, json=payload)
    assert res_post.status_code == 400
    assert res_post.get_json()["message"] == "Validation error"
    assert "error" in res_post.get_json()["errors"]


def test_create_client_db_error(client, monkeypatch, auth_headers):
    """Test database error during client creation"""
    def _boom():
        raise Exception("DB failure")
    monkeypatch.setattr("app.db.session.commit", _boom)

    payload = client_payload()
    resp = client.post("/clients", json=payload, headers=auth_headers)
    assert resp.status_code == 500
    assert resp.json["success"] is False
    assert "Error creating client" in resp.json["message"]


def test_get_clients(client, auth_headers):
    payload = client_payload()
    client.post("/clients", headers=auth_headers, json=payload)

    res_get = client.get("/clients", headers=auth_headers)
    assert res_get.status_code == 200
    assert res_get.get_json()["message"] == "Clients retrieved successfully"
    clients = res_get.get_json()["data"]["clients"]
    assert len(clients) >= 1  


def test_get_clients_empty(client, auth_headers):
    res_get = client.get("/clients", headers=auth_headers)
    assert res_get.status_code == 200
    assert res_get.get_json()["message"] == "Clients retrieved successfully"
    clients = res_get.get_json()["data"]["clients"]
    assert isinstance(clients, list)


def test_get_clients_error(client, monkeypatch, auth_headers):
    """Test exception during client list retrieval"""
    def _boom(*args, **kwargs):
        raise Exception("DB query error")
    monkeypatch.setattr("app.db.session.query", _boom)

    resp = client.get("/clients", headers=auth_headers)
    assert resp.status_code == 500
    assert resp.json["success"] is False
    assert "Error retrieving clients" in resp.json["message"]


def test_get_client_by_id(client, auth_headers):
    payload = client_payload()
    res_post = client.post("/clients", headers=auth_headers, json=payload)
    created_client = res_post.get_json()["data"]["client"]
    client_id = created_client["id"]

    res_get = client.get(f"/clients/{client_id}", headers=auth_headers)
    assert res_get.status_code == 200
    assert res_get.get_json()["message"] == "Client retrieved successfully"
    fetched_client = res_get.get_json()["data"]["client"]
    assert fetched_client["id"] == client_id
    for key in payload:
        assert fetched_client[key] == payload[key]
    

def test_get_client_by_id_not_found(client, auth_headers):
    non_existent_id = str(uuid4())
    res_get = client.get(f"/clients/{non_existent_id}", headers=auth_headers)
    assert res_get.status_code == 404
    assert res_get.get_json()["message"] == "Client not found"


def test_get_client_by_id_error(client, monkeypatch, auth_headers):
    """Test exception during individual client retrieval"""
    def _boom(*args, **kwargs):
        raise Exception("DB query error")
    monkeypatch.setattr("app.db.session.query", _boom)

    resp = client.get(f"/clients/{str(uuid4())}", headers=auth_headers)
    assert resp.status_code == 500
    assert resp.json["success"] is False
    assert "Error retrieving client" in resp.json["message"]


def test_update_patch_client(client, auth_headers):
    payload = client_payload()
    res_post = client.post("/clients", headers=auth_headers, json=payload)
    created_client = res_post.get_json()["data"]["client"]
    client_id = created_client["id"]

    update_payload = {
        "company_name": "Updated Company Name",
        "phone_number": "999-999-9999"
    }

    res_put = client.patch(f"/clients/{str(client_id)}", headers=auth_headers, json=update_payload)
    assert res_put.status_code == 200
    assert res_put.get_json()["message"] == "Client updated successfully"
    updated_client = res_put.get_json()["data"]["client"]
    assert updated_client["company_name"] == update_payload["company_name"]
    assert updated_client["phone_number"] == update_payload["phone_number"]
    assert updated_client["email"] == payload["email"]
    assert updated_client["address"] == payload["address"]


def test_update_patch_client_validation_error(client, auth_headers):
    payload = client_payload()
    res_post = client.post("/clients", headers=auth_headers, json=payload)
    created_client = res_post.get_json()["data"]["client"]
    client_id = created_client["id"]

    update_payload = {
        "email": "invalid-email"
    }

    res_patch = client.patch(f"/clients/{str(client_id)}", headers=auth_headers, json=update_payload)
    assert res_patch.status_code == 400
    assert res_patch.get_json()["message"] == "Validation error"
    assert "email" in res_patch.get_json()["errors"]


def test_update_patch_client_not_found(client, auth_headers):
    non_existent_id = str(uuid4())
    update_payload = {
        "company_name": "Updated Company Name"
    }
    res_patch = client.patch(f"/clients/{non_existent_id}", headers=auth_headers, json=update_payload)
    assert res_patch.status_code == 404
    assert res_patch.get_json()["message"] == "Client not found"


def test_update_patch_client_db_error(client, monkeypatch, auth_headers):
    """Test database error during client PATCH update"""
    payload = client_payload()
    res_post = client.post("/clients", headers=auth_headers, json=payload)
    created_client = res_post.get_json()["data"]["client"]
    client_id = created_client["id"]

    def _boom():
        raise Exception("DB failure")
    monkeypatch.setattr("app.db.session.commit", _boom)

    update_payload = {"company_name": "Updated"}
    resp = client.patch(f"/clients/{client_id}", headers=auth_headers, json=update_payload)
    assert resp.status_code == 500
    assert resp.json["success"] is False
    assert "Error updating client" in resp.json["message"]


def test_update_put_client(client, auth_headers):
    payload = client_payload()
    res_post = client.post("/clients", headers=auth_headers, json=payload)
    created_client = res_post.get_json()["data"]["client"]
    client_id = created_client["id"]

    update_payload = {
        "company_name": "Updated Company Name",
        "phone_number": "999-UP-DATED",
        "email": f"testclient-UPDATED@example.com",
        "address": "UPDATED Test St"

    }

    res_put = client.put(f"/clients/{str(client_id)}", headers=auth_headers, json=update_payload)
    assert res_put.status_code == 200
    assert res_put.get_json()["message"] == "Client updated successfully"
    updated_client = res_put.get_json()["data"]["client"]
    assert updated_client["company_name"] == update_payload["company_name"]
    assert updated_client["phone_number"] == update_payload["phone_number"]
    assert updated_client["email"] == update_payload["email"]
    assert updated_client["address"] == update_payload["address"]


def test_update_put_client_validation_error(client, auth_headers):
    payload = client_payload()
    res_post = client.post("/clients", headers=auth_headers, json=payload)
    created_client = res_post.get_json()["data"]["client"]
    client_id = created_client["id"]

    update_payload = {
        "company_name": "Updated Company Name",
        "phone_number": "999-UP-DATED",
        "email": "invalid-email",
        "address": "UPDATED Test St"
    }

    res_put = client.put(f"/clients/{str(client_id)}", headers=auth_headers, json=update_payload)
    assert res_put.status_code == 400
    assert res_put.get_json()["message"] == "Validation error"


def test_update_put_client_not_found(client, auth_headers):
    non_existent_id = str(uuid4())
    update_payload = {
        "company_name": "Updated Company Name",
        "phone_number": "999-999-9999",
        "email": "test@example.com",
        "address": "123 Test St"
    }
    res_put = client.put(f"/clients/{non_existent_id}", headers=auth_headers, json=update_payload)
    assert res_put.status_code == 404
    assert res_put.get_json()["message"] == "Client not found"


def test_update_put_client_db_error(client, monkeypatch, auth_headers):
    """Test database error during client PUT update"""
    payload = client_payload()
    res_post = client.post("/clients", headers=auth_headers, json=payload)
    created_client = res_post.get_json()["data"]["client"]
    client_id = created_client["id"]

    def _boom():
        raise Exception("DB failure")
    monkeypatch.setattr("app.db.session.commit", _boom)

    update_payload = {
        "company_name": "Updated",
        "phone_number": "999-999-9999",
        "email": "updated@example.com",
        "address": "Updated St"
    }
    resp = client.put(f"/clients/{client_id}", headers=auth_headers, json=update_payload)
    assert resp.status_code == 500
    assert resp.json["success"] is False
    assert "Error updating client" in resp.json["message"]


def test_delete_client(client, auth_headers):
    payload = client_payload()
    res_post = client.post("/clients", headers=auth_headers, json=payload)
    created_client = res_post.get_json()["data"]["client"]
    client_id = created_client["id"]

    res_delete = client.delete(f"/clients/{str(client_id)}", headers=auth_headers)
    assert res_delete.status_code == 200
    
    assert res_delete.get_json()["message"] == "Client archived successfully"
    archived_client = res_delete.get_json()["data"]["client"]
    assert archived_client["is_archived"] is True

    res_get = client.get("/clients", headers=auth_headers)
    assert res_get.status_code == 200
    clients = res_get.get_json()["data"]["clients"]
    client_ids = [c["id"] for c in clients]
    assert client_id not in client_ids


def test_delete_client_not_found(client, auth_headers):
    non_existent_id = str(uuid4())
    res_delete = client.delete(f"/clients/{non_existent_id}", headers=auth_headers)
    assert res_delete.status_code == 404
    assert res_delete.get_json()["message"] == "Client not found"


def test_delete_client_db_error(client, monkeypatch, auth_headers):
    """Test database error during client deletion"""
    payload = client_payload()
    res_post = client.post("/clients", headers=auth_headers, json=payload)
    created_client = res_post.get_json()["data"]["client"]
    client_id = created_client["id"]

    def _boom():
        raise Exception("DB failure")
    monkeypatch.setattr("app.db.session.commit", _boom)

    resp = client.delete(f"/clients/{client_id}", headers=auth_headers)
    assert resp.status_code == 500
    assert resp.json["success"] is False
    assert "Error archiving client" in resp.json["message"]


def test_archive_client_and_get(client, auth_headers):
    payload = client_payload()
    create = client.post("/clients", headers=auth_headers, json=payload)
    client_id = create.get_json()["data"]["client"]["id"]

    del_res = client.delete(f"/clients/{client_id}", headers=auth_headers)
    assert del_res.status_code == 200
    assert del_res.get_json()["data"]["client"]["is_archived"] is True
    
    get_res = client.get("/clients", headers=auth_headers)
    assert get_res.status_code == 200
    clients = get_res.get_json()["data"]["clients"]
    client_ids = [c["id"] for c in clients]
    assert client_id not in client_ids


def test_get_archived_client_by_id_not_found(client, auth_headers):
    """Test that archived clients cannot be retrieved by ID"""
    payload = client_payload()
    res_post = client.post("/clients", headers=auth_headers, json=payload)
    client_id = res_post.get_json()["data"]["client"]["id"]
    
    client.delete(f"/clients/{client_id}", headers=auth_headers)
    
    res_get = client.get(f"/clients/{client_id}", headers=auth_headers)
    assert res_get.status_code == 404
    assert res_get.get_json()["message"] == "Client not found"

def test_client_contracts(client, auth_headers):
    payload = client_payload()
    res_post = client.post("/clients", headers=auth_headers, json=payload)
    created_client = res_post.get_json()["data"]["client"]
    client_id = created_client["id"]

    res_get = client.get(f"/clients/{client_id}/contracts", headers=auth_headers)
    assert res_get.status_code == 200
    assert res_get.get_json()["message"] == "Contracts retrieved successfully"
    contracts = res_get.get_json()["data"]["contracts"]
    assert isinstance(contracts, list)


def test_client_contracts_not_found(client, auth_headers):
    """Test retrieving contracts for non-existent client"""
    non_existent_id = str(uuid4())
    res_get = client.get(f"/clients/{non_existent_id}/contracts", headers=auth_headers)
    assert res_get.status_code == 404
    assert res_get.get_json()["message"] == "Client not found"


def test_client_contracts_error(client, monkeypatch, auth_headers):
    """Test exception during client contracts retrieval"""
    payload = client_payload()
    res_post = client.post("/clients", headers=auth_headers, json=payload)
    created_client = res_post.get_json()["data"]["client"]
    client_id = created_client["id"]

    def _boom(*args, **kwargs):
        raise Exception("DB query error")
    monkeypatch.setattr("app.db.session.get", _boom)

    resp = client.get(f"/clients/{client_id}/contracts", headers=auth_headers)
    assert resp.status_code == 500
    assert resp.json["success"] is False
    assert "Error retrieving contracts" in resp.json["message"]