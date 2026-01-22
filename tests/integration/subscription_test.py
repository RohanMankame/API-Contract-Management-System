from tests.factories import (
    subscription_payload,
    create_subscription_dependencies,
    create_subscription_using_api,
    create_product_using_api,
    product_payload,
)
from uuid import uuid4


def test_create_subscription(client, auth_headers):
    """Test successful subscription creation"""
    deps = create_subscription_dependencies(client, auth_headers)
    contract_id = deps["contract"]["id"]
    product_id = deps["product"]["id"]
    
    payload = subscription_payload(contract_id, product_id)
    res = client.post("/subscriptions", headers=auth_headers, json=payload)
    assert res.status_code == 201
    assert res.get_json()["message"] == "Subscription created successfully"
    created_sub = res.get_json()["data"]["subscription"]
    assert created_sub["contract_id"] == contract_id
    assert created_sub["product_id"] == product_id
    assert created_sub["pricing_type"] == "Fixed"
    assert created_sub["strategy"] == "Fixed"


def test_create_subscription_missing_contract_id(client, auth_headers):
    """Test subscription creation without contract_id"""
    deps = create_subscription_dependencies(client, auth_headers)
    product_id = deps["product"]["id"]
    
    payload = {
        "product_id": str(product_id),
        "pricing_type": "Fixed",
        "strategy": "Fixed",
    }
    res = client.post("/subscriptions", headers=auth_headers, json=payload)
    assert res.status_code == 400
    assert res.get_json()["message"] == "Validation Error"
    assert "contract_id" in res.get_json()["errors"]


def test_create_subscription_missing_product_id(client, auth_headers):
    """Test subscription creation without product_id"""
    deps = create_subscription_dependencies(client, auth_headers)
    contract_id = deps["contract"]["id"]
    
    payload = {
        "contract_id": str(contract_id),
        "pricing_type": "Fixed",
        "strategy": "Fixed",
    }
    res = client.post("/subscriptions", headers=auth_headers, json=payload)
    assert res.status_code == 400
    assert res.get_json()["message"] == "Validation Error"
    assert "product_id" in res.get_json()["errors"]


def test_create_subscription_missing_pricing_type(client, auth_headers):
    """Test subscription creation without pricing_type"""
    deps = create_subscription_dependencies(client, auth_headers)
    contract_id = deps["contract"]["id"]
    product_id = deps["product"]["id"]
    
    payload = {
        "contract_id": str(contract_id),
        "product_id": str(product_id),
        "strategy": "Fixed",
    }
    res = client.post("/subscriptions", headers=auth_headers, json=payload)
    assert res.status_code == 400
    assert "pricing_type" in res.get_json()["errors"]


def test_create_subscription_missing_strategy(client, auth_headers):
    """Test subscription creation without strategy"""
    deps = create_subscription_dependencies(client, auth_headers)
    contract_id = deps["contract"]["id"]
    product_id = deps["product"]["id"]
    
    payload = {
        "contract_id": str(contract_id),
        "product_id": str(product_id),
        "pricing_type": "Fixed",
    }
    res = client.post("/subscriptions", headers=auth_headers, json=payload)
    assert res.status_code == 400
    assert "strategy" in res.get_json()["errors"]


def test_create_subscription_nonexistent_contract(client, auth_headers):
    """Test subscription creation with non-existent contract_id"""
    deps = create_subscription_dependencies(client, auth_headers)
    product_id = deps["product"]["id"]
    
    payload = subscription_payload(str(uuid4()), product_id)
    res = client.post("/subscriptions", headers=auth_headers, json=payload)
    assert res.status_code == 400
    assert res.get_json()["message"] == "Validation Error"
    assert "error" in res.get_json()["errors"]
    assert "Contract does not exist" in res.get_json()["errors"]["error"]


def test_create_subscription_nonexistent_product(client, auth_headers):
    """Test subscription creation with non-existent product_id"""
    deps = create_subscription_dependencies(client, auth_headers)
    contract_id = deps["contract"]["id"]
    
    payload = subscription_payload(contract_id, str(uuid4()))
    res = client.post("/subscriptions", headers=auth_headers, json=payload)
    assert res.status_code == 400
    assert res.get_json()["message"] == "Validation Error"
    assert "error" in res.get_json()["errors"]
    assert "Product does not exist" in res.get_json()["errors"]["error"]


def test_create_subscription_fixed_pricing_with_invalid_strategy(client, auth_headers):
    """Test Fixed pricing_type requires Fixed strategy"""
    deps = create_subscription_dependencies(client, auth_headers)
    contract_id = deps["contract"]["id"]
    product_id = deps["product"]["id"]
    
    payload = subscription_payload(contract_id, product_id, pricing_type="Fixed", strategy="Fill")
    res = client.post("/subscriptions", headers=auth_headers, json=payload)
    assert res.status_code == 400
    assert res.get_json()["message"] == "Validation Error"
    error_str = str(res.get_json()["errors"])
    assert "Strategy must be 'Fixed' when pricing_type is 'Fixed'." in error_str


def test_create_subscription_variable_pricing_fill_strategy(client, auth_headers):
    """Test Variable pricing_type with Fill strategy"""
    deps = create_subscription_dependencies(client, auth_headers)
    contract_id = deps["contract"]["id"]
    product_id = deps["product"]["id"]
    
    payload = subscription_payload(contract_id, product_id, pricing_type="Variable", strategy="Fill")
    res = client.post("/subscriptions", headers=auth_headers, json=payload)
    assert res.status_code == 201
    created_sub = res.get_json()["data"]["subscription"]
    assert created_sub["pricing_type"] == "Variable"
    assert created_sub["strategy"] == "Fill"


def test_create_subscription_variable_pricing_pick_strategy(client, auth_headers):
    """Test Variable pricing_type with Pick strategy"""
    deps = create_subscription_dependencies(client, auth_headers)
    contract_id = deps["contract"]["id"]
    product_id = deps["product"]["id"]
    
    payload = subscription_payload(contract_id, product_id, pricing_type="Variable", strategy="Pick")
    res = client.post("/subscriptions", headers=auth_headers, json=payload)
    assert res.status_code == 201
    created_sub = res.get_json()["data"]["subscription"]
    assert created_sub["pricing_type"] == "Variable"
    assert created_sub["strategy"] == "Pick"


def test_create_subscription_variable_pricing_flat_strategy(client, auth_headers):
    """Test Variable pricing_type with Flat strategy"""
    deps = create_subscription_dependencies(client, auth_headers)
    contract_id = deps["contract"]["id"]
    product_id = deps["product"]["id"]
    
    payload = subscription_payload(contract_id, product_id, pricing_type="Variable", strategy="Flat")
    res = client.post("/subscriptions", headers=auth_headers, json=payload)
    assert res.status_code == 201
    created_sub = res.get_json()["data"]["subscription"]
    assert created_sub["pricing_type"] == "Variable"
    assert created_sub["strategy"] == "Flat"


def test_create_subscription_testfail_product_validation(client, auth_headers):
    """Test subscription creation with TestFailSubscription product"""
    deps = create_subscription_dependencies(client, auth_headers)
    contract_id = deps["contract"]["id"]
    
    # Create a product with TestFailSubscription api_name
    product = create_product_using_api(client, auth_headers, product_payload(api_name="TestFailSubscription"))
    product_id = product["id"]
    
    payload = subscription_payload(contract_id, product_id)
    res = client.post("/subscriptions", headers=auth_headers, json=payload)
    assert res.status_code == 400
    assert res.get_json()["message"] == "Validation Error"
    assert "Cannot create subscription for product with api_name 'TestFailSubscription'" in str(res.get_json()["errors"])


def test_create_subscription_db_error(client, monkeypatch, auth_headers):
    """Test database error during subscription creation"""
    deps = create_subscription_dependencies(client, auth_headers)
    contract_id = deps["contract"]["id"]
    product_id = deps["product"]["id"]
    
    payload = subscription_payload(contract_id, product_id)
    
    def _boom():
        raise Exception("DB failure")
    monkeypatch.setattr("app.db.session.commit", _boom)
    
    resp = client.post("/subscriptions", headers=auth_headers, json=payload)
    assert resp.status_code == 500
    assert resp.json["success"] is False
    assert "Error creating subscription" in resp.json["message"]


def test_get_subscriptions(client, auth_headers):
    """Test retrieving all subscriptions"""
    deps = create_subscription_dependencies(client, auth_headers)
    contract_id = deps["contract"]["id"]
    product_id = deps["product"]["id"]
    
    create_subscription_using_api(client, auth_headers, contract_id, product_id)
    
    res = client.get("/subscriptions", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()["message"] == "Subscriptions fetched successfully"
    subscriptions = res.get_json()["data"]["subscriptions"]
    assert len(subscriptions) >= 1


def test_get_subscriptions_empty(client, auth_headers):
    """Test retrieving subscriptions when none exist"""
    res = client.get("/subscriptions", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()["message"] == "Subscriptions fetched successfully"
    subscriptions = res.get_json()["data"]["subscriptions"]
    assert isinstance(subscriptions, list)


def test_get_subscriptions_error(client, monkeypatch, auth_headers):
    """Test exception during subscriptions list retrieval"""
    def _boom(*args, **kwargs):
        raise Exception("DB query error")
    monkeypatch.setattr("app.db.session.query", _boom)

    resp = client.get("/subscriptions", headers=auth_headers)
    assert resp.status_code == 500
    assert resp.json["success"] is False
    assert "Error fetching subscriptions" in resp.json["message"]


def test_get_subscription_by_id(client, auth_headers):
    """Test retrieving a specific subscription by ID"""
    deps = create_subscription_dependencies(client, auth_headers)
    contract_id = deps["contract"]["id"]
    product_id = deps["product"]["id"]
    
    sub = create_subscription_using_api(client, auth_headers, contract_id, product_id)
    sub_id = sub["id"]
    
    res = client.get(f"/subscriptions/{sub_id}", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()["message"] == "Subscription fetched successfully"
    fetched_sub = res.get_json()["data"]["subscription"]
    assert fetched_sub["id"] == sub_id
    assert fetched_sub["contract_id"] == contract_id
    assert fetched_sub["product_id"] == product_id


def test_get_subscription_by_id_not_found(client, auth_headers):
    """Test retrieving non-existent subscription"""
    non_existent_id = str(uuid4())
    res = client.get(f"/subscriptions/{non_existent_id}", headers=auth_headers)
    assert res.status_code == 404
    assert res.get_json()["message"] == "Subscription not found"


def test_get_archived_subscription_by_id_not_found(client, auth_headers):
    """Test that archived subscriptions cannot be retrieved by ID (filtered view)"""
    deps = create_subscription_dependencies(client, auth_headers)
    contract_id = deps["contract"]["id"]
    product_id = deps["product"]["id"]
    
    sub = create_subscription_using_api(client, auth_headers, contract_id, product_id)
    sub_id = sub["id"]
    
    client.delete(f"/subscriptions/{sub_id}", headers=auth_headers)
    
    res = client.get(f"/subscriptions/{sub_id}", headers=auth_headers)
    assert res.status_code == 404
    assert res.get_json()["message"] == "Subscription not found"


def test_get_subscription_by_id_error(client, monkeypatch, auth_headers):
    """Test exception during subscription retrieval"""
    def _boom(*args, **kwargs):
        raise Exception("DB query error")
    monkeypatch.setattr("app.db.session.query", _boom)

    resp = client.get(f"/subscriptions/{str(uuid4())}", headers=auth_headers)
    assert resp.status_code == 500
    assert resp.json["success"] is False
    assert "Error getting subscription" in resp.json["message"]


def test_update_patch_subscription(client, auth_headers):
    """Test PATCH update of subscription"""
    deps = create_subscription_dependencies(client, auth_headers)
    contract_id = deps["contract"]["id"]
    product_id = deps["product"]["id"]
    
    sub = create_subscription_using_api(client, auth_headers, contract_id, product_id)
    sub_id = sub["id"]
    
    patch_payload = {
        "pricing_type": "Variable",
        "strategy": "Fill"
    }
    res = client.patch(f"/subscriptions/{sub_id}", headers=auth_headers, json=patch_payload)
    assert res.status_code == 200
    assert res.get_json()["message"] == "Subscription updated successfully"
    updated = res.get_json()["data"]["subscription"]
    assert updated["pricing_type"] == "Variable"
    assert updated["strategy"] == "Fill"


def test_update_patch_subscription_validation_error(client, auth_headers):
    """Test PATCH with validation error"""
    deps = create_subscription_dependencies(client, auth_headers)
    contract_id = deps["contract"]["id"]
    product_id = deps["product"]["id"]
    
    sub = create_subscription_using_api(client, auth_headers, contract_id, product_id)
    sub_id = sub["id"]
    
    patch_payload = {
        "pricing_type": "Fixed",
        "strategy": "Fill"  # Invalid: Fixed requires Fixed strategy
    }
    res = client.patch(f"/subscriptions/{sub_id}", headers=auth_headers, json=patch_payload)
    assert res.status_code == 400
    assert res.get_json()["message"] == "Validation Error"


def test_update_patch_subscription_not_found(client, auth_headers):
    """Test PATCH on non-existent subscription"""
    non_existent_id = str(uuid4())
    res = client.patch(f"/subscriptions/{non_existent_id}", headers=auth_headers, json={"pricing_type": "Variable"})
    assert res.status_code == 404
    assert res.get_json()["message"] == "Subscription not found"


def test_update_patch_subscription_db_error(client, monkeypatch, auth_headers):
    """Test database error during PATCH update"""
    deps = create_subscription_dependencies(client, auth_headers)
    contract_id = deps["contract"]["id"]
    product_id = deps["product"]["id"]
    
    sub = create_subscription_using_api(client, auth_headers, contract_id, product_id)
    sub_id = sub["id"]

    def _boom():
        raise Exception("DB failure")
    monkeypatch.setattr("app.db.session.commit", _boom)

    resp = client.patch(f"/subscriptions/{sub_id}", headers=auth_headers, json={"pricing_type": "Variable", "strategy": "Fill"})
    assert resp.status_code == 500
    assert resp.json["success"] is False
    assert "Error updating subscription" in resp.json["message"]


def test_update_put_subscription(client, auth_headers):
    """Test PUT update of subscription"""
    deps = create_subscription_dependencies(client, auth_headers)
    contract_id = deps["contract"]["id"]
    product_id = deps["product"]["id"]
    
    sub = create_subscription_using_api(client, auth_headers, contract_id, product_id)
    sub_id = sub["id"]
    
    put_payload = {
        "contract_id": str(contract_id),
        "product_id": str(product_id),
        "pricing_type": "Variable",
        "strategy": "Pick"
    }
    res = client.put(f"/subscriptions/{sub_id}", headers=auth_headers, json=put_payload)
    assert res.status_code == 200
    assert res.get_json()["message"] == "Subscription updated successfully"
    updated = res.get_json()["data"]["subscription"]
    assert updated["pricing_type"] == "Variable"
    assert updated["strategy"] == "Pick"


def test_update_put_subscription_validation_error(client, auth_headers):
    """Test PUT with validation error"""
    deps = create_subscription_dependencies(client, auth_headers)
    contract_id = deps["contract"]["id"]
    product_id = deps["product"]["id"]
    
    sub = create_subscription_using_api(client, auth_headers, contract_id, product_id)
    sub_id = sub["id"]
    
    put_payload = {
        "contract_id": str(contract_id),
        "product_id": str(product_id),
        "pricing_type": "Variable",
        "strategy": "Invalid"
    }
    res = client.put(f"/subscriptions/{sub_id}", headers=auth_headers, json=put_payload)
    assert res.status_code == 400
    assert res.get_json()["message"] == "Validation Error"


def test_update_put_subscription_not_found(client, auth_headers):
    """Test PUT on non-existent subscription"""
    non_existent_id = str(uuid4())
    put_payload = {
        "contract_id": str(uuid4()),
        "product_id": str(uuid4()),
        "pricing_type": "Fixed",
        "strategy": "Fixed"
    }
    res = client.put(f"/subscriptions/{non_existent_id}", headers=auth_headers, json=put_payload)
    assert res.status_code == 404
    assert res.get_json()["message"] == "Subscription not found"


def test_update_put_subscription_db_error(client, monkeypatch, auth_headers):
    """Test database error during PUT update"""
    deps = create_subscription_dependencies(client, auth_headers)
    contract_id = deps["contract"]["id"]
    product_id = deps["product"]["id"]
    
    sub = create_subscription_using_api(client, auth_headers, contract_id, product_id)
    sub_id = sub["id"]

    def _boom():
        raise Exception("DB failure")
    monkeypatch.setattr("app.db.session.commit", _boom)

    put_payload = {
        "contract_id": str(contract_id),
        "product_id": str(product_id),
        "pricing_type": "Variable",
        "strategy": "Fill"
    }
    resp = client.put(f"/subscriptions/{sub_id}", headers=auth_headers, json=put_payload)
    assert resp.status_code == 500
    assert resp.json["success"] is False
    assert "Error updating subscription" in resp.json["message"]


def test_delete_subscription(client, auth_headers):
    """Test subscription archival (soft delete)"""
    deps = create_subscription_dependencies(client, auth_headers)
    contract_id = deps["contract"]["id"]
    product_id = deps["product"]["id"]
    
    sub = create_subscription_using_api(client, auth_headers, contract_id, product_id)
    sub_id = sub["id"]
    
    res = client.delete(f"/subscriptions/{sub_id}", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()["message"] == "Subscription has been archived successfully"
    archived = res.get_json()["data"]["subscription"]
    assert archived["is_archived"] is True
    
    list_res = client.get("/subscriptions", headers=auth_headers)
    subscriptions = list_res.get_json()["data"]["subscriptions"]
    sub_ids = [s["id"] for s in subscriptions]
    assert sub_id not in sub_ids


def test_delete_subscription_not_found(client, auth_headers):
    """Test delete on non-existent subscription"""
    non_existent_id = str(uuid4())
    res = client.delete(f"/subscriptions/{non_existent_id}", headers=auth_headers)
    assert res.status_code == 404
    assert res.get_json()["message"] == "Subscription not found"


def test_delete_subscription_db_error(client, monkeypatch, auth_headers):
    """Test database error during subscription deletion"""
    deps = create_subscription_dependencies(client, auth_headers)
    contract_id = deps["contract"]["id"]
    product_id = deps["product"]["id"]
    
    sub = create_subscription_using_api(client, auth_headers, contract_id, product_id)
    sub_id = sub["id"]

    def _boom():
        raise Exception("DB failure")
    monkeypatch.setattr("app.db.session.commit", _boom)

    resp = client.delete(f"/subscriptions/{sub_id}", headers=auth_headers)
    assert resp.status_code == 500
    assert resp.json["success"] is False
    assert "Error archiving subscription" in resp.json["message"]