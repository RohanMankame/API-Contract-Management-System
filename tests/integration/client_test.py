
from tests.factories import client_payload
from uuid import uuid4

def test_create_client(client, auth_headers):
    payload = client_payload()
    res_post = client.post("/clients", headers=auth_headers, json=payload)
    assert res_post.status_code == 201
    assert res_post.get_json()["message"] == "Client created successfully"
    created_client = res_post.get_json()["data"]["client"]
    for key in payload:
        assert created_client[key] == payload[key]
    


def test_get_clients(client, auth_headers):
    payload = client_payload()
    client.post("/clients", headers=auth_headers, json=payload)

    res_get = client.get("/clients", headers=auth_headers)
    assert res_get.status_code == 200
    assert res_get.get_json()["message"] == "Clients retrieved successfully"
    clients = res_get.get_json()["data"]["clients"]
    assert len(clients) >= 1  



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

    res_put = client.patch(f"/clients/{str(client_id)}", headers=auth_headers, json=update_payload)
    assert res_put.status_code == 200
    assert res_put.get_json()["message"] == "Client updated successfully"
    updated_client = res_put.get_json()["data"]["client"]
    assert updated_client["company_name"] == update_payload["company_name"]
    assert updated_client["phone_number"] == update_payload["phone_number"]
    assert updated_client["email"] == update_payload["email"]
    assert updated_client["address"] == update_payload["address"]




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

    res_get = client.get(f"/clients/{str(client_id)}", headers=auth_headers)
    assert res_get.status_code == 200
    fetched_client = res_get.get_json()["data"]["client"]
    assert fetched_client["is_archived"] is True



def test_delete_client_not_found(client, auth_headers):
    non_existent_id = str(uuid4())
    res_delete = client.delete(f"/clients/{non_existent_id}", headers=auth_headers)
    assert res_delete.status_code == 404
    assert res_delete.get_json()["message"] == "Client not found"




def test_archive_client_and_get(client, auth_headers):
    payload = client_payload()
    create = client.post("/clients", headers=auth_headers, json=payload)
    client_id = create.get_json()["data"]["client"]["id"]

    del_res = client.delete(f"/clients/{client_id}", headers=auth_headers)
    assert del_res.status_code == 200
    assert del_res.get_json()["data"]["client"]["is_archived"] is True
    
    get_res = client.get(f"/clients/{client_id}", headers=auth_headers)
    assert get_res.status_code == 200
    assert get_res.get_json()["data"]["client"]["is_archived"] is True