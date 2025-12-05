

'''

def test_contract(client, auth_headers):
    """
    Test creating a contract and then retrieving it.
    """
    # POST
    post_res = client.post("/Contracts", headers=auth_headers, json={
        "client_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "contract_name": "Contract A",
        })
    
    assert post_res.status_code == 201

    # GET
    get_res = client.get("/Contracts", headers=auth_headers)
    assert get_res.status_code == 200
    data = get_res.get_json()
    assert "contracts" in data

    contract = data["contracts"][0]
    assert contract["contract_name"] == "Contract A"
    assert contract["client_id"] == "3fa85f64-5717-4562-b3fc-2c963f66afa6"
   


## for /Contracts/<id>
def test_contract_by_id(client, auth_headers):
    """
    Test creating a contract and then retrieving, updating, and deleting it by ID."""
    post_res = client.post("/Contracts", headers=auth_headers, json={
        "client_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "contract_name": "Contract B",
        
        })
    
    assert post_res.status_code == 201

    contract_id = post_res.get_json()["contract"]["id"]

    assert contract_id is not None
    assert isinstance(contract_id, str)

    # GET by ID
    get_res = client.get(f"/Contracts/{contract_id}", headers=auth_headers)
    assert get_res.status_code == 200

    data = get_res.get_json()
    assert "contract" in data
    contract_data = data["contract"]
    assert contract_data["id"] == contract_id
    assert contract_data["contract_name"] == "Contract B"
    assert contract_data["client_id"] == "3fa85f64-5717-4562-b3fc-2c963f66afa6"

    # PUT by ID
    put_res = client.put(f"/Contracts/{contract_id}", headers=auth_headers, json={
        "contract_name": "Contract B Updated"
        })
    assert put_res.status_code == 200
    updated_data = put_res.get_json()
    assert updated_data["message"] == "Contract updated successfully"
'''