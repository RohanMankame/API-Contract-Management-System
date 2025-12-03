

## for /Clients
def test_client(client, auth_headers):
    """
    Test creating a client and then retrieving it.
    """
    # POST
    post_res = client.post("/Clients", headers=auth_headers, json={
        "company_name": "Test Client",
        "email": "testclient@LionRentals.com",
        "phone_number": "555-555-5555",
        "address": "123 Test St, Test City"
        })
    
    assert post_res.status_code == 201

    # GET
    get_res = client.get("/Clients", headers=auth_headers)
    assert get_res.status_code == 200
    data = get_res.get_json()
    assert "clients" in data

    client = data["clients"][0]
    assert client["company_name"] == "Test Client"
    assert client["email"] == "testclient@LionRentals.com"
    assert client["phone_number"] == "555-555-5555"
    assert client["address"] == "123 Test St, Test City"
    





## for /Clients/<id>
def test_client_by_id(client, auth_headers):
    """
    Test creating a client and then retrieving, updating, and deleting it by ID."""
    post_res = client.post("/Clients", headers=auth_headers, json={
        "company_name": "Test Client 2",
        "email": "testclient2@LionRentals.com",
        "phone_number": "555-555-5556",
        "address": "124 Test St, Test City"
        })
    
    assert post_res.status_code == 201

    client_id = post_res.get_json()["client"]["id"]

    assert client_id is not None
    assert isinstance(client_id, str)

    # GET by ID
    get_res = client.get(f"/Clients/{client_id}", headers=auth_headers)
    assert get_res.status_code == 200

    data = get_res.get_json()
    assert "client" in data
    client_data = data["client"]
    assert client_data["id"] == client_id

    # PUT and PATCH by ID
    put_res = client.put(f"/Clients/{client_id}", headers=auth_headers, json={
        "phone_number": "999-999-9999"
    })
    assert put_res.status_code == 200
    updated_data = put_res.get_json()["client"]
    assert updated_data["phone_number"] == "999-999-9999"

    print(updated_data["is_archived"] )

    # DELETE by ID
    delete_res = client.delete(f"/Clients/{client_id}", headers=auth_headers)
    assert delete_res.status_code == 200

    get_res = client.get(f"/Clients/{client_id}", headers=auth_headers)
    assert get_res.status_code == 200

    get_res = get_res.get_json()["client"]
    print(get_res)
    assert get_res["is_archived"] == True
    