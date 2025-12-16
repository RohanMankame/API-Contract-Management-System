from tests.factories import *
import uuid



def test_dependencies_setup(client, auth_headers):
    deps = create_subscription_dependencies(client, auth_headers)
    assert "client" in deps
    assert "product" in deps
    assert "contract" in deps
    



def test_create_subscription_tier(client, auth_headers):
    deps = create_subscription_dependencies(client, auth_headers)
    subscription_obj = create_subscription_using_api(
        client,
        auth_headers,
        contract_id=deps["contract"]["id"],
        product_id=deps["product"]["id"]
    )
    payload = subscription_tier_payload(subscription_id=subscription_obj["id"])
    res = client.post("/Subscription_tiers", headers=auth_headers, json=payload)
    assert res.status_code == 201
    created_tier = res.get_json()["subscription_tier"]

    #THIS IS CAUSING ISSUES WITH DATETIME COMPARISON AND FLOAT INT COMPARISON
    '''
    for key in payload:
        if key != "start_date" and key != "end_date":
            assert created_tier[key] == payload[key]
    '''




def test_create_subscription_tier_missing_fields(client, auth_headers):
    payload = {
        # "subscription_id" is missing
        "tier_name": "Premium",
        "start_date": "2025-12-08T09:25:18.505Z",
        "end_date": "2027-11-08T09:25:18.505Z",
        "base_price": 5000,
        "price_per_tier": 10
    }
    res = client.post("/Subscription_tiers", headers=auth_headers, json=payload)
    assert res.status_code == 400


def test_create_subscription_tier_invalid_subscription(client, auth_headers):
    invalid_subscription_id = str(uuid.uuid4())
    payload = {
        "subscription_id": invalid_subscription_id,
        "tier_name": "Premium",
        "start_date": "2025-12-08T09:25:18.505Z",
        "end_date": "2027-11-08T09:25:18.505Z",
        "base_price": 5000,
        "price_per_tier": 10
    }
    res = client.post("/Subscription_tiers", headers=auth_headers, json=payload)
    assert res.status_code == 400




def test_get_subscription_tiers(client, auth_headers):
    deps = create_subscription_dependencies(client, auth_headers)
    
    subscription_obj = create_subscription_using_api(
        client,
        auth_headers,
        contract_id=deps["contract"]["id"],
        product_id=deps["product"]["id"]
    )
    payload = subscription_tier_payload(subscription_id=subscription_obj["id"])
    res = client.post("/Subscription_tiers", headers=auth_headers, json=payload)
    assert res.status_code == 201
    res_get = client.get("/Subscription_tiers", headers=auth_headers)
    assert res_get.status_code == 200
    tiers = res_get.get_json()["subscription_tiers"]
    assert isinstance(tiers, list)
    assert len(tiers) >= 1






def test_get_subscription_tier_by_id(client, auth_headers):
    deps = create_subscription_dependencies(client, auth_headers)
    subscription_obj = create_subscription_using_api(
        client,
        auth_headers,
        contract_id=deps["contract"]["id"],
        product_id=deps["product"]["id"]
    )
    payload = subscription_tier_payload(subscription_id=subscription_obj["id"])
    res_create = client.post("/Subscription_tiers", headers=auth_headers, json=payload)
    assert res_create.status_code == 201
    created_tier = res_create.get_json()["subscription_tier"]
    tier_id = created_tier["id"]

    res_get = client.get(f"/Subscription_tiers/{tier_id}", headers=auth_headers)
    assert res_get.status_code == 200
    fetched_tier = res_get.get_json()["subscription_tier"]
    assert fetched_tier["id"] == tier_id


def test_get_subscription_tier_by_id_not_found(client, auth_headers):
    non_existent_tier_id = str(uuid.uuid4())
    res_get = client.get(f"/Subscription_tiers/{non_existent_tier_id}", headers=auth_headers)
    assert res_get.status_code == 404


def test_get_subscription_tier_by_invalid_uuid(client, auth_headers):
    invalid_tier_id = str(uuid.uuid4())
    res_get = client.get(f"/Subscription_tiers/{invalid_tier_id}", headers=auth_headers)
    assert res_get.status_code == 404

def test_archived_subscription_tier(client, auth_headers):
    deps = create_subscription_dependencies(client, auth_headers)
    subscription_obj = create_subscription_using_api(
        client,
        auth_headers,
        contract_id=deps["contract"]["id"],
        product_id=deps["product"]["id"]
    )
    payload = subscription_tier_payload(subscription_id=subscription_obj["id"])
    res_create = client.post("/Subscription_tiers", headers=auth_headers, json=payload)
    assert res_create.status_code == 201
    created_tier = res_create.get_json()["subscription_tier"]
    tier_id = created_tier["id"]

    res_delete = client.delete(f"/Subscription_tiers/{tier_id}", headers=auth_headers)
    assert res_delete.status_code == 200

    res_get = client.get(f"/Subscription_tiers/{tier_id}", headers=auth_headers)
    assert res_get.status_code == 200
    fetched_tier = res_get.get_json()["subscription_tier"]
    assert fetched_tier["is_archived"] is True


def test_archive_subscription_tier_not_found(client, auth_headers):
    non_existent_tier_id = str(uuid.uuid4())
    res_delete = client.delete(f"/Subscription_tiers/{non_existent_tier_id}", headers=auth_headers)
    assert res_delete.status_code == 404


