from tests.factories import (
    contract_payload,
    client_payload,
    create_client_using_api,
    create_contract_using_api,
    create_subscription_dependencies,
    create_subscription_using_api,
    product_payload,
    create_product_using_api
)
from uuid import uuid4



def test_create_contract(client, auth_headers):
    """Test successful contract creation"""
    client_obj = create_client_using_api(client, auth_headers)
    payload = contract_payload(client_obj["id"])
    
    res = client.post("/contracts", headers=auth_headers, json=payload)
    assert res.status_code == 201
    assert res.get_json()["message"] == "Contract created successfully"
    created_contract = res.get_json()["data"]["contract"]
    assert created_contract["contract_name"] == payload["contract_name"]
    assert created_contract["client_id"] == str(client_obj["id"])


def test_create_contract_missing_client_id(client, auth_headers):
    """Test contract creation without client_id"""
    payload = {
        "contract_name": "Test Contract",
        "start_date": "2025-01-01T00:00:00.000Z",
        "end_date": "2026-12-31T23:59:59.999Z",
    }
    res = client.post("/contracts", headers=auth_headers, json=payload)
    assert res.status_code == 400
    assert res.get_json()["message"] == "Validation Error"
    assert "client_id" in res.get_json()["errors"]


def test_create_contract_missing_contract_name(client, auth_headers):
    """Test contract creation without contract_name"""
    client_obj = create_client_using_api(client, auth_headers)
    payload = {
        "client_id": str(client_obj["id"]),
        "start_date": "2025-01-01T00:00:00.000Z",
        "end_date": "2026-12-31T23:59:59.999Z",
    }
    res = client.post("/contracts", headers=auth_headers, json=payload)
    assert res.status_code == 400
    assert "contract_name" in res.get_json()["errors"]


def test_create_contract_missing_start_date(client, auth_headers):
    """Test contract creation without start_date"""
    client_obj = create_client_using_api(client, auth_headers)
    payload = {
        "client_id": str(client_obj["id"]),
        "contract_name": "Test",
        "end_date": "2026-12-31T23:59:59.999Z",
    }
    res = client.post("/contracts", headers=auth_headers, json=payload)
    assert res.status_code == 400
    assert "start_date" in res.get_json()["errors"]


def test_create_contract_missing_end_date(client, auth_headers):
    """Test contract creation without end_date"""
    client_obj = create_client_using_api(client, auth_headers)
    payload = {
        "client_id": str(client_obj["id"]),
        "contract_name": "Test",
        "start_date": "2025-01-01T00:00:00.000Z",
    }
    res = client.post("/contracts", headers=auth_headers, json=payload)
    assert res.status_code == 400
    assert "end_date" in res.get_json()["errors"]


def test_create_contract_nonexistent_client(client, auth_headers):
    """Test contract creation with non-existent client_id"""
    payload = contract_payload(str(uuid4()))
    res = client.post("/contracts", headers=auth_headers, json=payload)
    assert res.status_code == 400
    assert res.get_json()["message"] == "Validation Error"
    assert "error" in res.get_json()["errors"]


def test_create_contract_end_date_before_start_date(client, auth_headers):
    """Test contract creation with end_date before start_date"""
    client_obj = create_client_using_api(client, auth_headers)
    payload = {
        "client_id": str(client_obj["id"]),
        "contract_name": "Test",
        "start_date": "2026-12-31T23:59:59.999Z",
        "end_date": "2025-01-01T00:00:00.000Z",
    }
    res = client.post("/contracts", headers=auth_headers, json=payload)
    assert res.status_code == 400
    assert "error" in res.get_json()["errors"]
    assert "End date must be after start date" in res.get_json()["errors"]["error"]


def test_create_contract_testfail_validation(client, auth_headers):
    """Test contract creation with TestFailContract name"""
    client_obj = create_client_using_api(client, auth_headers)
    payload = contract_payload(client_obj["id"], contract_name="TestFailContract")
    res = client.post("/contracts", headers=auth_headers, json=payload)
    assert res.status_code == 400
    assert "error" in res.get_json()["errors"]


def test_create_contract_db_error(client, monkeypatch, auth_headers):
    """Test database error during contract creation"""
    client_obj = create_client_using_api(client, auth_headers)
    payload = contract_payload(client_obj["id"])
    
    def _boom():
        raise Exception("DB failure")
    monkeypatch.setattr("app.db.session.commit", _boom)
    
    resp = client.post("/contracts", headers=auth_headers, json=payload)
    assert resp.status_code == 500
    assert resp.json["success"] is False
    assert "Error creating contract" in resp.json["message"]



def test_get_contracts(client, auth_headers):
    """Test retrieving all contracts"""
    client_obj = create_client_using_api(client, auth_headers)
    create_contract_using_api(client, auth_headers, client_obj["id"])
    
    res = client.get("/contracts", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()["message"] == "Contracts fetched successfully"
    contracts = res.get_json()["data"]["contracts"]
    assert len(contracts) >= 1


def test_get_contracts_empty(client, auth_headers):
    """Test retrieving contracts when none exist"""
    res = client.get("/contracts", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()["message"] == "Contracts fetched successfully"
    contracts = res.get_json()["data"]["contracts"]
    assert isinstance(contracts, list)


def test_get_contracts_error(client, monkeypatch, auth_headers):
    """Test exception during contracts list retrieval"""
    def _boom(*args, **kwargs):
        raise Exception("DB query error")
    monkeypatch.setattr("app.db.session.query", _boom)

    resp = client.get("/contracts", headers=auth_headers)
    assert resp.status_code == 500
    assert resp.json["success"] is False
    assert "Error fetching contracts" in resp.json["message"]


def test_get_contract_by_id(client, auth_headers):
    """Test retrieving a specific contract by ID"""
    client_obj = create_client_using_api(client, auth_headers)
    contract = create_contract_using_api(client, auth_headers, client_obj["id"])
    contract_id = contract["id"]
    
    res = client.get(f"/contracts/{contract_id}", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()["message"] == "Contract fetched successfully"
    fetched_contract = res.get_json()["data"]["contract"]
    assert fetched_contract["id"] == contract_id
    assert fetched_contract["contract_name"] == contract["contract_name"]


def test_get_contract_by_id_not_found(client, auth_headers):
    """Test retrieving non-existent contract"""
    non_existent_id = str(uuid4())
    res = client.get(f"/contracts/{non_existent_id}", headers=auth_headers)
    assert res.status_code == 404
    assert res.get_json()["message"] == "Contract not found"


def test_get_archived_contract_by_id_not_found(client, auth_headers):
    """Test that archived contracts cannot be retrieved by ID (filtered view)"""
    client_obj = create_client_using_api(client, auth_headers)
    contract = create_contract_using_api(client, auth_headers, client_obj["id"])
    contract_id = contract["id"]
    
    client.delete(f"/contracts/{contract_id}", headers=auth_headers)
    
    res = client.get(f"/contracts/{contract_id}", headers=auth_headers)
    assert res.status_code == 404
    assert res.get_json()["message"] == "Contract not found"


def test_get_contract_by_id_error(client, monkeypatch, auth_headers):
    """Test exception during contract retrieval"""
    def _boom(*args, **kwargs):
        raise Exception("DB query error")
    monkeypatch.setattr("app.db.session.query", _boom)

    resp = client.get(f"/contracts/{str(uuid4())}", headers=auth_headers)
    assert resp.status_code == 500
    assert resp.json["success"] is False
    assert "Error getting contract" in resp.json["message"]



def test_update_patch_contract(client, auth_headers):
    """Test PATCH update of contract"""
    client_obj = create_client_using_api(client, auth_headers)
    contract = create_contract_using_api(client, auth_headers, client_obj["id"])
    contract_id = contract["id"]
    
    patch_payload = {
        "contract_name": "Updated Contract Name"
    }
    res = client.patch(f"/contracts/{contract_id}", headers=auth_headers, json=patch_payload)
    assert res.status_code == 200
    assert res.get_json()["message"] == "Contract updated successfully"
    updated = res.get_json()["data"]["contract"]
    assert updated["contract_name"] == "Updated Contract Name"


def test_update_patch_contract_validation_error(client, auth_headers):
    """Test PATCH with validation error"""
    client_obj = create_client_using_api(client, auth_headers)
    contract = create_contract_using_api(client, auth_headers, client_obj["id"])
    contract_id = contract["id"]
    
    patch_payload = {
        "contract_name": "TestFailContract"
    }
    res = client.patch(f"/contracts/{contract_id}", headers=auth_headers, json=patch_payload)
    assert res.status_code == 400
    assert res.get_json()["message"] == "Validation Error"


def test_update_patch_contract_not_found(client, auth_headers):
    """Test PATCH on non-existent contract"""
    non_existent_id = str(uuid4())
    res = client.patch(f"/contracts/{non_existent_id}", headers=auth_headers, json={"contract_name": "Updated"})
    assert res.status_code == 404
    assert res.get_json()["message"] == "Contract not found"


def test_update_patch_contract_db_error(client, monkeypatch, auth_headers):
    """Test database error during PATCH update"""
    client_obj = create_client_using_api(client, auth_headers)
    contract = create_contract_using_api(client, auth_headers, client_obj["id"])
    contract_id = contract["id"]

    def _boom():
        raise Exception("DB failure")
    monkeypatch.setattr("app.db.session.commit", _boom)

    resp = client.patch(f"/contracts/{contract_id}", headers=auth_headers, json={"contract_name": "Updated"})
    assert resp.status_code == 500
    assert resp.json["success"] is False
    assert "Error updating contract" in resp.json["message"]


def test_update_put_contract(client, auth_headers):
    """Test PUT update of contract"""
    client_obj = create_client_using_api(client, auth_headers)
    contract = create_contract_using_api(client, auth_headers, client_obj["id"])
    contract_id = contract["id"]
    
    put_payload = {
        "client_id": str(client_obj["id"]),
        "contract_name": "Updated Contract",
        "start_date": "2025-06-01T00:00:00.000Z",
        "end_date": "2026-06-01T00:00:00.000Z"
    }
    res = client.put(f"/contracts/{contract_id}", headers=auth_headers, json=put_payload)
    assert res.status_code == 200
    assert res.get_json()["message"] == "Contract updated successfully"
    updated = res.get_json()["data"]["contract"]
    assert updated["contract_name"] == "Updated Contract"


def test_update_put_contract_validation_error(client, auth_headers):
    """Test PUT with validation error (end date before start)"""
    client_obj = create_client_using_api(client, auth_headers)
    contract = create_contract_using_api(client, auth_headers, client_obj["id"])
    contract_id = contract["id"]
    
    put_payload = {
        "client_id": str(client_obj["id"]),
        "contract_name": "Updated",
        "start_date": "2026-12-31T00:00:00.000Z",
        "end_date": "2025-01-01T00:00:00.000Z"
    }
    res = client.put(f"/contracts/{contract_id}", headers=auth_headers, json=put_payload)
    assert res.status_code == 400
    assert res.get_json()["message"] == "Validation Error"


def test_update_put_contract_not_found(client, auth_headers):
    """Test PUT on non-existent contract"""
    non_existent_id = str(uuid4())
    put_payload = {
        "client_id": str(uuid4()),
        "contract_name": "Updated",
        "start_date": "2025-01-01T00:00:00.000Z",
        "end_date": "2026-12-31T00:00:00.000Z"
    }
    res = client.put(f"/contracts/{non_existent_id}", headers=auth_headers, json=put_payload)
    assert res.status_code == 404
    assert res.get_json()["message"] == "Contract not found"


def test_update_put_contract_db_error(client, monkeypatch, auth_headers):
    """Test database error during PUT update"""
    client_obj = create_client_using_api(client, auth_headers)
    contract = create_contract_using_api(client, auth_headers, client_obj["id"])
    contract_id = contract["id"]

    def _boom():
        raise Exception("DB failure")
    monkeypatch.setattr("app.db.session.commit", _boom)

    put_payload = {
        "client_id": str(client_obj["id"]),
        "contract_name": "Updated",
        "start_date": "2025-01-01T00:00:00.000Z",
        "end_date": "2026-12-31T00:00:00.000Z"
    }
    resp = client.put(f"/contracts/{contract_id}", headers=auth_headers, json=put_payload)
    assert resp.status_code == 500
    assert resp.json["success"] is False
    assert "Error updating contract" in resp.json["message"]


def test_delete_contract(client, auth_headers):
    """Test contract archival (soft delete)"""
    client_obj = create_client_using_api(client, auth_headers)
    contract = create_contract_using_api(client, auth_headers, client_obj["id"])
    contract_id = contract["id"]
    
    res = client.delete(f"/contracts/{contract_id}", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()["message"] == "Contract has been archived successfully"
    archived = res.get_json()["data"]["contract"]
    assert archived["is_archived"] is True
    
    # Verify archived contract is NOT in list
    list_res = client.get("/contracts", headers=auth_headers)
    contracts = list_res.get_json()["data"]["contracts"]
    contract_ids = [c["id"] for c in contracts]
    assert contract_id not in contract_ids


def test_delete_contract_not_found(client, auth_headers):
    """Test delete on non-existent contract"""
    non_existent_id = str(uuid4())
    res = client.delete(f"/contracts/{non_existent_id}", headers=auth_headers)
    assert res.status_code == 404
    assert res.get_json()["message"] == "Contract not found"


def test_delete_contract_db_error(client, monkeypatch, auth_headers):
    """Test database error during contract deletion"""
    client_obj = create_client_using_api(client, auth_headers)
    contract = create_contract_using_api(client, auth_headers, client_obj["id"])
    contract_id = contract["id"]

    def _boom():
        raise Exception("DB failure")
    monkeypatch.setattr("app.db.session.commit", _boom)

    resp = client.delete(f"/contracts/{contract_id}", headers=auth_headers)
    assert resp.status_code == 500
    assert resp.json["success"] is False
    assert "Error deleting contract" in resp.json["message"]


def test_contract_products_empty(client, auth_headers):
    """Test retrieving products for contract with no subscriptions"""
    client_obj = create_client_using_api(client, auth_headers)
    contract = create_contract_using_api(client, auth_headers, client_obj["id"])
    contract_id = contract["id"]
    
    res = client.get(f"/contracts/{contract_id}/product", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()["message"] == "Products fetched successfully"
    products = res.get_json()["data"]["products"]
    assert isinstance(products, list)
    assert len(products) == 0


def test_contract_products_with_subscription(client, auth_headers):
    """Test retrieving products for contract with subscriptions
    Covers: for subscription in contract.subscriptions: product = subscription.product"""
    deps = create_subscription_dependencies(client, auth_headers)
    contract_id = deps["contract"]["id"]
    product_id = deps["product"]["id"]
    
    # Create subscription linking contract to product
    create_subscription_using_api(client, auth_headers, contract_id, product_id)
    
    res = client.get(f"/contracts/{contract_id}/product", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()["message"] == "Products fetched successfully"
    products = res.get_json()["data"]["products"]
    assert len(products) == 1
    assert products[0]["id"] == product_id


def test_contract_products_with_multiple_subscriptions_same_product(client, auth_headers):
    """Test product deduplication via unique_products dict"""
    deps = create_subscription_dependencies(client, auth_headers)
    contract_id = deps["contract"]["id"]
    product_id = deps["product"]["id"]
    
    # Create two subscriptions for same product
    create_subscription_using_api(client, auth_headers, contract_id, product_id)
    create_subscription_using_api(client, auth_headers, contract_id, product_id)
    
    res = client.get(f"/contracts/{contract_id}/product", headers=auth_headers)
    assert res.status_code == 200
    products = res.get_json()["data"]["products"]
    # Should only have 1 product (deduplication works)
    assert len(products) == 1
    assert products[0]["id"] == product_id


def test_contract_products_with_multiple_subscriptions_different_products(client, auth_headers):
    """Test retrieving multiple different products"""
    client_obj = create_client_using_api(client, auth_headers)
    contract = create_contract_using_api(client, auth_headers, client_obj["id"])
    contract_id = contract["id"]
    
    # Create two products
    product1 = create_product_using_api(client, auth_headers)
    product2 = create_product_using_api(client, auth_headers)
    product1_id = product1["id"]
    product2_id = product2["id"]
    
    # Create subscriptions for both products
    create_subscription_using_api(client, auth_headers, contract_id, product1_id)
    create_subscription_using_api(client, auth_headers, contract_id, product2_id)
    
    res = client.get(f"/contracts/{contract_id}/product", headers=auth_headers)
    assert res.status_code == 200
    products = res.get_json()["data"]["products"]
    assert len(products) == 2
    product_ids = [p["id"] for p in products]
    assert product1_id in product_ids
    assert product2_id in product_ids


def test_contract_products_not_found(client, auth_headers):
    """Test retrieving products for non-existent contract"""
    non_existent_id = str(uuid4())
    res = client.get(f"/contracts/{non_existent_id}/product", headers=auth_headers)
    assert res.status_code == 404
    assert res.get_json()["message"] == "Contract not found"


def test_contract_products_error(client, monkeypatch, auth_headers):
    """Test exception during products retrieval"""
    client_obj = create_client_using_api(client, auth_headers)
    contract = create_contract_using_api(client, auth_headers, client_obj["id"])
    contract_id = contract["id"]

    def _boom(*args, **kwargs):
        raise Exception("DB query error")
    monkeypatch.setattr("app.db.session.get", _boom)

    resp = client.get(f"/contracts/{contract_id}/product", headers=auth_headers)
    assert resp.status_code == 500
    assert resp.json["success"] is False
    assert "Error getting products" in resp.json["message"]


def test_contract_subscriptions_empty(client, auth_headers):
    """Test retrieving subscriptions for contract with no subscriptions"""
    client_obj = create_client_using_api(client, auth_headers)
    contract = create_contract_using_api(client, auth_headers, client_obj["id"])
    contract_id = contract["id"]
    
    res = client.get(f"/contracts/{contract_id}/subscriptions", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()["message"] == "Subscriptions fetched successfully"
    subscriptions = res.get_json()["data"]["subscriptions"]
    assert isinstance(subscriptions, list)
    assert len(subscriptions) == 0


def test_contract_subscriptions_get(client, auth_headers):
    """Test retrieving subscriptions for contract"""
    deps = create_subscription_dependencies(client, auth_headers)
    contract_id = deps["contract"]["id"]
    product_id = deps["product"]["id"]
    
    sub = create_subscription_using_api(client, auth_headers, contract_id, product_id)
    
    res = client.get(f"/contracts/{contract_id}/subscriptions", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()["message"] == "Subscriptions fetched successfully"
    subscriptions = res.get_json()["data"]["subscriptions"]
    assert len(subscriptions) == 1
    assert subscriptions[0]["id"] == sub["id"]


def test_contract_subscriptions_post(client, auth_headers):
    """Test creating subscription for contract"""
    client_obj = create_client_using_api(client, auth_headers)
    contract = create_contract_using_api(client, auth_headers, client_obj["id"])
    product = create_product_using_api(client, auth_headers)
    contract_id = contract["id"]
    product_id = product["id"]
    
    payload = {
        "product_id": str(product_id),
        "pricing_type": "Fixed",
        "strategy": "Fixed"
    }
    res = client.post(f"/contracts/{contract_id}/subscriptions", headers=auth_headers, json=payload)
    assert res.status_code == 201
    assert res.get_json()["message"] == "Subscription created successfully"
    sub = res.get_json()["data"]["subscription"]
    assert sub["contract_id"] == contract_id
    assert sub["product_id"] == product_id


def test_contract_subscriptions_post_archived_product(client, auth_headers):
    """Test creating subscription with archived product"""
    client_obj = create_client_using_api(client, auth_headers)
    contract = create_contract_using_api(client, auth_headers, client_obj["id"])
    product = create_product_using_api(client, auth_headers)
    contract_id = contract["id"]
    product_id = product["id"]
    
    client.delete(f"/products/{product_id}", headers=auth_headers)
    
    payload = {
        "product_id": str(product_id),
        "pricing_type": "Fixed",
        "strategy": "Fixed"
    }
    res = client.post(f"/contracts/{contract_id}/subscriptions", headers=auth_headers, json=payload)
    assert res.status_code == 400
    assert "Product not found or is archived" in res.get_json()["message"]


def test_contract_subscriptions_not_found(client, auth_headers):
    """Test subscriptions endpoint on non-existent contract"""
    non_existent_id = str(uuid4())
    res = client.get(f"/contracts/{non_existent_id}/subscriptions", headers=auth_headers)
    assert res.status_code == 404
    assert res.get_json()["message"] == "Contract not found"


def test_contract_subscriptions_post_not_found(client, auth_headers):
    """Test POST subscriptions on non-existent contract"""
    non_existent_id = str(uuid4())
    payload = {
        "product_id": str(uuid4()),
        "pricing_type": "Fixed",
        "strategy": "Fixed"
    }
    res = client.post(f"/contracts/{non_existent_id}/subscriptions", headers=auth_headers, json=payload)
    assert res.status_code == 404
    assert res.get_json()["message"] == "Contract not found"


def test_contract_subscriptions_post_validation_error(client, auth_headers):
    """Test POST subscriptions with validation error"""
    client_obj = create_client_using_api(client, auth_headers)
    contract = create_contract_using_api(client, auth_headers, client_obj["id"])
    contract_id = contract["id"]
    
    payload = {
        "product_id": str(uuid4()),
        # Missing pricing_type and strategy
    }
    res = client.post(f"/contracts/{contract_id}/subscriptions", headers=auth_headers, json=payload)
    assert res.status_code == 400
    assert res.get_json()["message"] == "Validation Error"


def test_contract_subscriptions_post_db_error(client, monkeypatch, auth_headers):
    """Test database error during subscription creation"""
    client_obj = create_client_using_api(client, auth_headers)
    contract = create_contract_using_api(client, auth_headers, client_obj["id"])
    product = create_product_using_api(client, auth_headers)
    contract_id = contract["id"]
    product_id = product["id"]

    def _boom():
        raise Exception("DB failure")
    monkeypatch.setattr("app.db.session.commit", _boom)

    payload = {
        "product_id": str(product_id),
        "pricing_type": "Fixed",
        "strategy": "Fixed"
    }
    resp = client.post(f"/contracts/{contract_id}/subscriptions", headers=auth_headers, json=payload)
    assert resp.status_code == 500
    assert resp.json["success"] is False
    assert "Error processing subscriptions" in resp.json["message"]