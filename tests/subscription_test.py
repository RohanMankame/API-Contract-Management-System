
# for /Subscriptions


def test_subscription(client, auth_headers):
    """
    Test creating a subscription and then retrieving it.
    """
    # POST
    post_res = client.post("/Subscriptions", headers=auth_headers, json={
        "contract_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "product_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "pricing_type": "Fixed",
        "strategy": "Fixed"
    })
    
    assert post_res.status_code == 201  
    
    # GET
    get_res = client.get("/Subscriptions", headers=auth_headers)
    assert get_res.status_code == 200
    data = get_res.get_json()
    assert "subscriptions" in data
    subscription = data["subscriptions"][0]
    assert subscription["contract_id"] == "3fa85f64-5717-4562-b3fc-2c963f66afa6"




# for /Subscriptions/<id>
def test_subscription_by_id(client, auth_headers):
    """
    Test creating a subscription and then retrieving, updating, and deleting it by ID."""
    post_res = client.post("/Subscriptions", headers=auth_headers, json={
        "contract_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "product_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "pricing_type": "Fixed",
        "strategy": "Fixed"
    })
    
    assert post_res.status_code == 201

    subscription_id = post_res.get_json()["subscription"]["id"]

    assert subscription_id is not None
    assert isinstance(subscription_id, str)
    print("Subscription ID is: " + subscription_id)
    

    # GET by ID
    get_res = client.get(f"/Subscriptions/{subscription_id}", headers=auth_headers)
    assert get_res.status_code == 200

    data = get_res.get_json()
    assert "subscription" in data
    subscription_data = data["subscription"]
    assert subscription_data["id"] == subscription_id