from tests.factories import create_subscription_dependencies, subscription_payload
import uuid


def test_create_subscription(client, auth_headers):
    deps = create_subscription_dependencies(client, auth_headers)
    payload = subscription_payload(contract_id=deps["contract"]["id"], product_id=deps["product"]["id"])
    res = client.post("/Subscriptions", headers=auth_headers, json=payload)
    assert res.status_code == 201
    created_subscription = res.get_json()["subscription"]
    for key in payload:
        assert created_subscription[key] == payload[key]
    

def test_create_subscription_invalid_product(client, auth_headers):
    deps = create_subscription_dependencies(client, auth_headers)
    invalid_product_id = str(uuid.uuid4())
    payload = subscription_payload(contract_id=deps["contract"]["id"], product_id=invalid_product_id)
    res = client.post("/Subscriptions", headers=auth_headers, json=payload)
    assert res.status_code == 400


def test_create_subscription_invalid_contract(client, auth_headers):
    deps = create_subscription_dependencies(client, auth_headers)
    invalid_contract_id = str(uuid.uuid4())
    payload = subscription_payload(contract_id=invalid_contract_id, product_id=deps["product"]["id"])
    res = client.post("/Subscriptions", headers=auth_headers, json=payload)
    assert res.status_code == 400



def test_create_subscription_missing_fields(client, auth_headers):
    payload = {
        # "contract_id" is missing
        "product_id": str(uuid.uuid4()),
        "pricing_type": "Fixed",
        "strategy": "Fixed",
    }
    res = client.post("/Subscriptions", headers=auth_headers, json=payload)
    assert res.status_code == 400



def test_get_subscriptions(client, auth_headers):
    res = client.get("/Subscriptions", headers=auth_headers)
    assert res.status_code == 200
    subscriptions = res.get_json()["subscriptions"]
    assert isinstance(subscriptions, list)
    assert len(subscriptions) >= 0



def test_get_subscription_by_id(client, auth_headers):
    deps = create_subscription_dependencies(client, auth_headers)
    payload = subscription_payload(contract_id=deps["contract"]["id"], product_id=deps["product"]["id"])
    res_create = client.post("/Subscriptions", headers=auth_headers, json=payload)
    created_subscription = res_create.get_json()["subscription"]
    subscription_id = created_subscription["id"]

    res_get = client.get(f"/Subscriptions/{subscription_id}", headers=auth_headers)
    assert res_get.status_code == 200
    fetched_subscription = res_get.get_json()["subscription"]
    assert fetched_subscription["id"] == subscription_id
    for key in payload:
        assert fetched_subscription[key] == payload[key]




def test_get_subscription_by_id_not_found(client, auth_headers):
    non_existent_id = str(uuid.uuid4())
    res = client.get(f"/Subscriptions/{non_existent_id}", headers=auth_headers)
    assert res.status_code == 404
    assert res.get_json()["error"] == "Subscription not found"


def test_get_subscription_by_id_invalid_uuid(client, auth_headers):
    invalid_id = "invalid-uuid"
    res = client.get(f"/Subscriptions/{invalid_id}", headers=auth_headers)
    assert res.status_code == 400
    assert res.get_json()["error"] == "Error getting subscription"


def test_archive_subscription(client, auth_headers):
    deps = create_subscription_dependencies(client, auth_headers)
    payload = subscription_payload(contract_id=deps["contract"]["id"], product_id=deps["product"]["id"])
    res_create = client.post("/Subscriptions", headers=auth_headers, json=payload)
    created_subscription = res_create.get_json()["subscription"]
    subscription_id = created_subscription["id"]

    res_delete = client.delete(f"/Subscriptions/{subscription_id}", headers=auth_headers)
    assert res_delete.status_code == 200
    assert res_delete.get_json()["message"] == "Subscription has been archived successfully"

    res_get = client.get(f"/Subscriptions/{subscription_id}", headers=auth_headers)
    assert res_get.status_code == 200
    fetched_subscription = res_get.get_json()["subscription"]
    assert fetched_subscription["is_archived"] is True


def test_archive_subscription_not_found(client, auth_headers):
    non_existent_id = str(uuid.uuid4())
    res = client.delete(f"/Subscriptions/{non_existent_id}", headers=auth_headers)
    assert res.status_code == 404
    assert res.get_json()["error"] == "Subscription not found"


