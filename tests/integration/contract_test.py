from tests.factories import contract_payload, client_payload
import uuid

def test_create_contract(client, auth_headers):
    # create client for contract
    client_payload_data = client_payload()
    res_client = client.post("/clients", headers=auth_headers, json=client_payload_data)
    created_client = res_client.get_json()["data"]["client"]
    client_id = created_client["id"]

    # create contract with the client_id
    payload = contract_payload(client_id=client_id)
    res_post = client.post("/contracts", headers=auth_headers, json=payload)

    assert res_post.status_code == 201
    assert res_post.get_json()["message"] == "Contract created successfully"
    created_contract = res_post.get_json()["data"]["contract"]
    for key in payload:
        assert created_contract[key] == payload[key]


def test_get_contracts(client, auth_headers):
    # create client for contract
    client_payload_data = client_payload()
    res_client = client.post("/clients", headers=auth_headers, json=client_payload_data)
    created_client = res_client.get_json()["data"]["client"]
    client_id = created_client["id"]

    # create contract with the client_id
    payload = contract_payload(client_id=client_id)
    client.post("/contracts", headers=auth_headers, json=payload)

    res_get = client.get("/contracts", headers=auth_headers)
    assert res_get.status_code == 200
    assert res_get.get_json()["message"] == "Contracts fetched successfully"
    contracts = res_get.get_json()["data"]["contracts"]
    assert len(contracts) >= 1



def test_get_contract_by_id(client, auth_headers):
    # create client for contract
    client_payload_data = client_payload()
    res_client = client.post("/clients", headers=auth_headers, json=client_payload_data)
    created_client = res_client.get_json()["data"]["client"]
    client_id = created_client["id"]

    # create contract with the client_id
    payload = contract_payload(client_id=client_id)
    res_post = client.post("/contracts", headers=auth_headers, json=payload)
    created_contract = res_post.get_json()["data"]["contract"]
    contract_id = created_contract["id"]

    res_get = client.get(f"/contracts/{contract_id}", headers=auth_headers)
    assert res_get.status_code == 200
    assert res_get.get_json()["message"] == "Contract fetched successfully"
    fetched_contract = res_get.get_json()["data"]["contract"]
    assert fetched_contract["id"] == contract_id
    for key in payload:
        assert fetched_contract[key] == payload[key]




def test_get_contract_by_id_not_found(client, auth_headers):
    non_existent_id = str(uuid.uuid4())
    res_get = client.get(f"/contracts/{non_existent_id}", headers=auth_headers)
    assert res_get.status_code == 404
    assert res_get.get_json()["message"] == "Contract not found"



def test_update_patch_contract(client, auth_headers):
    # create client for contract
    client_payload_data = client_payload()
    res_client = client.post("/clients", headers=auth_headers, json=client_payload_data)
    created_client = res_client.get_json()["data"]["client"]
    client_id = created_client["id"]

    # create contract with the client_id
    payload = contract_payload(client_id=client_id)
    res_post = client.post("/contracts", headers=auth_headers, json=payload)
    created_contract = res_post.get_json()["data"]["contract"]
    contract_id = created_contract["id"]

    update_payload = {
        "contract_name": "Updated Contract Name"
    }

    res_put = client.patch(f"/contracts/{str(contract_id)}", headers=auth_headers, json=update_payload)
    assert res_put.status_code == 200
    assert res_put.get_json()["message"] == "Contract updated successfully"
    updated_contract = res_put.get_json()["data"]["contract"]
    assert updated_contract["contract_name"] == update_payload["contract_name"]
    

def test_update_put_contract(client, auth_headers):
    # create client for contract
    client_payload_data = client_payload()
    res_client = client.post("/clients", headers=auth_headers, json=client_payload_data)
    created_client = res_client.get_json()["data"]["client"]
    client_id = created_client["id"]

    # create contract with the client_id
    payload = contract_payload(client_id=client_id)
    res_post = client.post("/contracts", headers=auth_headers, json=payload)
    created_contract = res_post.get_json()["data"]["contract"]
    contract_id = created_contract["id"]

    update_payload = {
        "contract_name": "Updated Contract Name"
    }

    res_put = client.patch(f"/contracts/{str(contract_id)}", headers=auth_headers, json=update_payload)
    assert res_put.status_code == 200
    assert res_put.get_json()["message"] == "Contract updated successfully"
    updated_contract = res_put.get_json()["data"]["contract"]
    assert updated_contract["contract_name"] == update_payload["contract_name"]
    

def test_delete_contract(client, auth_headers):
    # create client for contract
    client_payload_data = client_payload()
    res_client = client.post("/clients", headers=auth_headers, json=client_payload_data)
    created_client = res_client.get_json()["data"]["client"]
    client_id = created_client["id"]

    # create contract with the client_id
    payload = contract_payload(client_id=client_id)
    res_post = client.post("/contracts", headers=auth_headers, json=payload)
    created_contract = res_post.get_json()["data"]["contract"]
    contract_id = created_contract["id"]

    res_delete = client.delete(f"/contracts/{contract_id}", headers=auth_headers)
    assert res_delete.status_code == 200
    assert res_delete.get_json()["message"] == "Contract has been archived successfully"

    res_get = client.get(f"/contracts/{contract_id}", headers=auth_headers)
    assert res_get.status_code == 200
    fetched_contract = res_get.get_json()["data"]["contract"]
    assert fetched_contract["is_archived"] == True


def test_delete_contract_not_found(client, auth_headers):
    non_existent_id = str(uuid.uuid4())
    res_delete = client.delete(f"/contracts/{non_existent_id}", headers=auth_headers)
    assert res_delete.status_code == 404
    assert res_delete.get_json()["message"] == "Contract not found"


    