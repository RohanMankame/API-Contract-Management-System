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



"""
def test_create_subscription(client, auth_headers):
    # create a client
    client_data = client_payload()
    res_client = client.post("/Clients", headers=auth_headers, json=client_data)
    created_client = res_client.get_json()["client"]
    client_id = created_client["id"]

    # create a contract 
    contract_data = contract_payload(client_id)
    res_contract = client.post("/Contracts", headers=auth_headers, json=contract_data)
    created_contract = res_contract.get_json()["contract"]
    contract_id = created_contract["id"]

    # create a product
    product_data = product_payload()
    res_product = client.post("/Products", headers=auth_headers, json=product_data)
    created_product = res_product.get_json()["product"]
    product_id = created_product["id"]

    # Now, create a subscription for the contract and product
    subscription_data = subscription_payload(contract_id, product_id)
    res_subscription = client.post("/Subscriptions", headers=auth_headers, json=subscription_data)
    assert res_subscription.status_code == 201
    assert res_subscription.get_json()["message"] == "Subscription created successfully"
    created_subscription = res_subscription.get_json()["subscription"]
    for key in subscription_data:
        assert created_subscription[key] == subscription_data[key]


def test_create_subscription_invalid_contract(client, auth_headers):
    # create a product
    product_data = product_payload()
    res_product = client.post("/Products", headers=auth_headers, json=product_data)
    created_product = res_product.get_json()["product"]
    product_id = created_product["id"]

    # use fake contract
    invalid_contract_id = str(uuid.uuid4())
    subscription_data = subscription_payload(invalid_contract_id, product_id)
    res_subscription = client.post("/Subscriptions", headers=auth_headers, json=subscription_data)
    assert res_subscription.status_code == 400
    

def test_get_subscriptions(client, auth_headers):
    res_get = client.get("/Subscriptions", headers=auth_headers)
    assert res_get.status_code == 200
    assert res_get.get_json()["message"] == "Subscriptions fetched successfully"
    subscriptions = res_get.get_json()["subscriptions"]
    assert isinstance(subscriptions, list)


def test_get_subscription_by_id(client, auth_headers):
    # create a client
    client_data = client_payload()
    res_client = client.post("/Clients", headers=auth_headers, json=client_data)
    created_client = res_client.get_json()["client"]
    client_id = created_client["id"]

    # create a contract 
    contract_data = contract_payload(client_id)
    res_contract = client.post("/Contracts", headers=auth_headers, json=contract_data)
    created_contract = res_contract.get_json()["contract"]
    contract_id = created_contract["id"]

    # create a product
    product_data = product_payload()
    res_product = client.post("/Products", headers=auth_headers, json=product_data)
    created_product = res_product.get_json()["product"]
    product_id = created_product["id"]

    # Now, create a subscription for the contract and product
    subscription_data = subscription_payload(contract_id, product_id)
    res_subscription = client.post("/Subscriptions", headers=auth_headers, json=subscription_data)
    created_subscription = res_subscription.get_json()["subscription"]
    subscription_id = created_subscription["id"]

    # Fetch the subscription by ID
    res_get = client.get(f"/Subscriptions/{subscription_id}", headers=auth_headers)
    assert res_get.status_code == 200
    fetched_subscription = res_get.get_json()["subscription"]
    assert fetched_subscription["id"] == subscription_id
    for key in subscription_data:
        assert fetched_subscription[key] == subscription_data[key]


def test_get_subscription_by_id_not_found(client, auth_headers):
    non_existent_id = str(uuid.uuid4())
    res_get = client.get(f"/Subscriptions/{non_existent_id}", headers=auth_headers)
    assert res_get.status_code == 404
    assert res_get.get_json()["error"] == "Subscription not found"

    """