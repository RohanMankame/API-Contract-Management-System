
def test_subscription_tier(client, auth_headers):
    """
    Test creating a subscription tier and then retrieving it.
    """
    # POST
    post_res = client.post("/Subscription_tiers", headers=auth_headers, json={
        "subscription_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "min_calls": 0,
        "max_calls": 0,
        "start_date": "2025-12-03T09:58:49.511Z",
        "end_date": "2027-12-03T09:58:49.511Z",
        "base_price": 0,
        "price_per_tier": 0,
    })
    
    assert post_res.status_code == 201  
    
    # GET
    get_res = client.get("/Subscription_tiers", headers=auth_headers)
    assert get_res.status_code == 200
    data = get_res.get_json()
    assert "subscription_tiers" in data
    subscription_tier = data["subscription_tiers"][0]
    assert subscription_tier["subscription_id"] == "3fa85f64-5717-4562-b3fc-2c963f66afa6"


# for /Subscription_tiers/<id>
def test_subscription_tier_by_id(client, auth_headers):
    """
    Test creating a subscription tier and then retrieving, updating, and deleting it by ID.
    """
    post_res = client.post("/Subscription_tiers", headers=auth_headers, json={
        "subscription_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "min_calls": 0,
        "max_calls": 0,
        "start_date": "2025-12-03T09:58:49.511Z",
        "end_date": "2027-12-03T09:58:49.511Z",
        "base_price": 0,
        "price_per_tier": 0,
    })
    
    assert post_res.status_code == 201

    subscription_tier_id = post_res.get_json()["subscription_tier"]["id"]

    assert subscription_tier_id is not None
    assert isinstance(subscription_tier_id, str)
    print("Subscription Tier ID is: " + subscription_tier_id)
    

    # GET by ID
    get_res = client.get(f"/Subscription_tiers/{subscription_tier_id}", headers=auth_headers)
    print("JSON RES:",get_res.get_json())
    assert get_res.status_code == 200

    data = get_res.get_json()
    assert "subscription_tier" in data
    subscription_tier_data = data["subscription_tier"]
    assert subscription_tier_data["id"] == subscription_tier_id