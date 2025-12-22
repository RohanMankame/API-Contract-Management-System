from tests.factories import create_subscription_dependencies, subscription_payload
from uuid import uuid4



def test_create_subscription(client, auth_headers):
    deps = create_subscription_dependencies(client, auth_headers)
    payload = subscription_payload(contract_id=deps["contract"]["id"], product_id=deps["product"]["id"])
    
    res = client.post("/subscriptions", headers=auth_headers, json=payload)
    assert res.status_code == 201
    assert res.get_json()["message"] == "Subscription created successfully"
    created_subscription = res.get_json()["data"]["subscription"]
    for key in payload:
        assert created_subscription[key] == payload[key]




def test_create_subscription_invalid_product(client, auth_headers):
    deps = create_subscription_dependencies(client, auth_headers)
    invalid_product_id = str(uuid4())
    payload = subscription_payload(contract_id=deps["contract"]["id"], product_id=invalid_product_id)
    res = client.post("/subscriptions", headers=auth_headers, json=payload)
    assert res.status_code == 400


def test_create_subscription_invalid_contract(client, auth_headers):
    deps = create_subscription_dependencies(client, auth_headers)
    invalid_contract_id = str(uuid4())
    payload = subscription_payload(contract_id=invalid_contract_id, product_id=deps["product"]["id"])
    res = client.post("/subscriptions", headers=auth_headers, json=payload)
    assert res.status_code == 400



def test_create_subscription_missing_fields(client, auth_headers):
    payload = {
        # "contract_id" is missing
        "product_id": str(  uuid4()),
        "pricing_type": "Fixed",
        "strategy": "Fixed",
    }
    res = client.post("/subscriptions", headers=auth_headers, json=payload)
    assert res.status_code == 400



def test_get_subscriptions(client, auth_headers):
    res = client.get("/subscriptions", headers=auth_headers)
    assert res.status_code == 200
    subscriptions = res.get_json()["data"]["subscriptions"]
    assert isinstance(subscriptions, list)
    assert len(subscriptions) >= 0



def test_get_subscription_by_id(client, auth_headers):
    deps = create_subscription_dependencies(client, auth_headers)
    payload = subscription_payload(contract_id=deps["contract"]["id"], product_id=deps["product"]["id"])
    res_create = client.post("/subscriptions", headers=auth_headers, json=payload)
    created_subscription = res_create.get_json()["data"]["subscription"]
    subscription_id = created_subscription["id"]

    res_get = client.get(f"/subscriptions/{subscription_id}", headers=auth_headers)
    assert res_get.status_code == 200
    fetched_subscription = res_get.get_json()["data"]["subscription"]
    assert fetched_subscription["id"] == subscription_id
    for key in payload:
        assert fetched_subscription[key] == payload[key]




def test_get_subscription_by_id_not_found(client, auth_headers):
    non_existent_id = str(uuid4())
    res = client.get(f"/subscriptions/{non_existent_id}", headers=auth_headers)
    assert res.status_code == 404
    assert res.get_json()["message"] == "Subscription not found"


def test_get_subscription_by_id_invalid_uuid(client, auth_headers):
    invalid_id = "invalid-uuid"
    res = client.get(f"/subscriptions/{invalid_id}", headers=auth_headers)
    assert res.status_code == 500
    assert res.get_json()["message"] == "Error getting subscription"


def test_archive_subscription(client, auth_headers):
    deps = create_subscription_dependencies(client, auth_headers)
    payload = subscription_payload(contract_id=deps["contract"]["id"], product_id=deps["product"]["id"])
    res_create = client.post("/subscriptions", headers=auth_headers, json=payload)
    created_subscription = res_create.get_json()["data"]["subscription"]
    subscription_id = created_subscription["id"]

    res_delete = client.delete(f"/subscriptions/{subscription_id}", headers=auth_headers)
    assert res_delete.status_code == 200
    assert res_delete.get_json()["message"] == "Subscription has been archived successfully"

    res_get = client.get(f"/subscriptions/{subscription_id}", headers=auth_headers)
    assert res_get.status_code == 200
    fetched_subscription = res_get.get_json()["data"]["subscription"]
    assert fetched_subscription["is_archived"] is True


def test_update_subscription(client, auth_headers):
    deps = create_subscription_dependencies(client, auth_headers)
    payload = subscription_payload(contract_id=deps["contract"]["id"], product_id=deps["product"]["id"])
    
    res = client.post("/subscriptions", headers=auth_headers, json=payload)
    assert res.status_code == 201
    assert res.get_json()["message"] == "Subscription created successfully"
    created_subscription = res.get_json()["data"]["subscription"]
    for key in payload:
        assert created_subscription[key] == payload[key]

    updated_res = client.patch(f"/subscriptions/{created_subscription['id']}", headers=auth_headers, json={
        "pricing_type": "Variable"
        })
    assert updated_res.status_code == 200




def test_archive_subscription_not_found(client, auth_headers):
    non_existent_id = str(uuid4())
    res = client.delete(f"/subscriptions/{non_existent_id}", headers=auth_headers)
    assert res.status_code == 404
    assert res.get_json()["message"] == "Subscription not found"



def test_subscription_invalid_parent_ids(client, auth_headers):
    invalid_uuid = str(uuid4())
    payload = subscription_payload(contract_id=invalid_uuid, product_id=invalid_uuid)
    res = client.post("/subscriptions", headers=auth_headers, json=payload)
    assert res.status_code == 400
    assert "message" in res.get_json()
    assert res.get_json()["message"] == "Validation Error"


def test_protected_endpoints_require_auth(client):
    res = client.get("/subscriptions")
    assert res.status_code == 401
