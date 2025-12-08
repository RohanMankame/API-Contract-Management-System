from tests.factories import user_payload
import uuid

def test_create_user(client, auth_headers):
    payload = user_payload()
    res_post = client.post("/Users", headers=auth_headers, json=payload)

    assert res_post.status_code == 201
    assert res_post.get_json()["message"] == "User created successfully"
    created_user = res_post.get_json()["user"]
    for key in payload:
        if key != "password":  
            assert created_user[key] == payload[key]


def test_get_users(client, auth_headers):
    payload = user_payload()
    client.post("/Users", headers=auth_headers, json=payload)

    res_get = client.get("/Users", headers=auth_headers)
    assert res_get.status_code == 200
    assert res_get.get_json()["message"] == "Users retrieved successfully"
    users = res_get.get_json()["users"]
    assert len(users) >= 1



def test_get_user_by_id(client, auth_headers): 
    payload = user_payload()
    res_post = client.post("/Users", headers=auth_headers, json=payload)
    created_user = res_post.get_json()["user"]
    user_id = created_user["id"]

    res_get = client.get(f"/Users/{user_id}", headers=auth_headers)
    assert res_get.status_code == 200
    assert res_get.get_json()["message"] == "User retrieved successfully"
    fetched_user = res_get.get_json()["user"]
    assert fetched_user["id"] == user_id
    for key in payload:
        if key != "password":  
            assert fetched_user[key] == payload[key]


def test_get_user_by_id_not_found(client, auth_headers):
    non_existent_id = str(uuid.uuid4())
    res_get = client.get(f"/Users/{non_existent_id}", headers=auth_headers)
    assert res_get.status_code == 404
    assert res_get.get_json()["error"] == "User not found"



def test_update_patch_user(client, auth_headers):
    payload = user_payload()
    res_post = client.post("/Users", headers=auth_headers, json=payload)
    created_user = res_post.get_json()["user"]
    user_id = created_user["id"]

    update_payload = {
        "full_name": "Updated User Name",
    }

    res_put = client.put(f"/Users/{user_id}", headers=auth_headers, json=update_payload)
    assert res_put.status_code == 200
    updated_user = res_put.get_json()["user"]
    assert updated_user["full_name"] == "Updated User Name"


def test_update_put_user(client, auth_headers):
    payload = user_payload()
    res_post = client.post("/Users", headers=auth_headers, json=payload)
    created_user = res_post.get_json()["user"]
    user_id = created_user["id"]

    update_payload = {
        "full_name": "Updated User Name",
        "email": "updatedemail@example.com"
    }

    res_put = client.put(f"/Users/{user_id}", headers=auth_headers, json=update_payload)
    assert res_put.status_code == 200
    updated_user = res_put.get_json()["user"]
    assert updated_user["full_name"] == "Updated User Name"
    assert updated_user["email"] == "updatedemail@example.com"


def test_delete_user(client, auth_headers):
    payload = user_payload()
    res_post = client.post("/Users", headers=auth_headers, json=payload)
    created_user = res_post.get_json()["user"]
    user_id = created_user["id"]

    res_delete = client.delete(f"/Users/{user_id}", headers=auth_headers)
    assert res_delete.status_code == 200
    assert res_delete.get_json()["message"] == "User archived successfully"

    res_get = client.get(f"/Users/{user_id}", headers=auth_headers)
    assert res_get.status_code == 200
    fetched_user = res_get.get_json()["user"]
    assert fetched_user["is_archived"] is True


def test_delete_user_not_found(client, auth_headers):
    non_existent_id = str(uuid.uuid4())
    res_delete = client.delete(f"/Users/{non_existent_id}", headers=auth_headers)
    assert res_delete.status_code == 404
    assert res_delete.get_json()["error"] == "User not found"