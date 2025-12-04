
def test_user(client, auth_headers):
    """
    Test creating a user and then retrieving it.
    """
    

    # POST
    post_res = client.post("/Users", headers=auth_headers, json={
        "full_name": "Rohan Mankame",
        "email": "Rohan@gmail.com",
        "password": "pass12345"
        })
    
    print(post_res.get_json())
    
    assert post_res.status_code == 201
    
    # GET
    get_res = client.get("/Users", headers=auth_headers)
    assert get_res.status_code == 200
    data = get_res.get_json()
    assert "users" in data

    user = data["users"][0]
    assert user["full_name"] == "Test User"
    




## for /Users/<id>
def test_user_by_id(client, auth_headers):
    """
    Test creating a user and then retrieving, updating, and deleting it by ID.
    """
    post_res = client.post("/Users", headers=auth_headers, json={
        "full_name": "Rohan Mankame",
        "email": "Rohan@gmail.com",
        "password": "pass12345"
        })
    
    assert post_res.status_code == 201

    user_id = post_res.get_json()["user"]["id"]

    assert user_id is not None
    assert isinstance(user_id, str)

    # GET by ID
    get_res = client.get(f"/Users/{user_id}", headers=auth_headers)
    assert get_res.status_code == 200

    data = get_res.get_json()
    assert "user" in data
    user_data = data["user"]
    assert user_data["id"] == user_id

    # PUT and PATCH by ID
    put_res = client.put(f"/Users/{user_id}", headers=auth_headers, json={
        "full_name": "Rohan Mankame 2",
    })
    assert put_res.status_code == 200
    updated_data = put_res.get_json()

    # DELETE by ID
    delete_res = client.delete(f"/Users/{user_id}", headers=auth_headers)
    assert delete_res.status_code == 200

    get_res = client.get(f"/Users/{user_id}", headers=auth_headers)
    assert get_res.status_code == 200

    get_res = get_res.get_json()["user"]
    print(get_res)
    assert get_res["is_archived"] == True
    