from tests.factories import (
    product_payload, 
    create_subscription_dependencies,
    create_subscription_using_api
)
from uuid import uuid4


def test_create_product(client, auth_headers):
    payload = product_payload()
    res_post = client.post("/products", headers=auth_headers, json=payload)

    assert res_post.status_code == 201
    assert res_post.get_json()["message"] == "Product created successfully"
    created_product = res_post.get_json()["data"]["product"]
    for key in payload:
        assert created_product[key] == payload[key]


def test_create_product_missing_api_name(client, auth_headers):
    payload = {
        "description": "A sample product description."
    }
    res_post = client.post("/products", headers=auth_headers, json=payload)
    assert res_post.status_code == 400
    assert res_post.get_json()["message"] == "Validation Error"
    assert "api_name" in res_post.get_json()["errors"]


def test_create_product_testfail_validation(client, auth_headers):
    payload = product_payload()
    payload["api_name"] = "TestFailProduct"
    res_post = client.post("/products", headers=auth_headers, json=payload)
    
    assert res_post.status_code == 400
    assert res_post.get_json()["message"] == "Validation Error"
    assert "error" in res_post.get_json()["errors"]


def test_create_product_duplicate_api_name(client, auth_headers):
    payload = product_payload(api_name="UniqueProductName")
    
    # Create first product
    res1 = client.post("/products", headers=auth_headers, json=payload)
    assert res1.status_code == 201
    
    # Try to create duplicate
    res2 = client.post("/products", headers=auth_headers, json=payload)
    assert res2.status_code == 400
    assert "already exists" in res2.get_json()["message"]


def test_create_product_db_error(client, monkeypatch, auth_headers):
    """Test database error during product creation"""
    def _boom():
        raise Exception("DB failure")
    monkeypatch.setattr("app.db.session.commit", _boom)
    
    payload = product_payload()
    resp = client.post("/products", headers=auth_headers, json=payload)
    assert resp.status_code == 500
    assert resp.json["success"] is False
    assert "Error creating product" in resp.json["message"]


def test_get_products(client, auth_headers):
    payload = product_payload()
    client.post("/products", headers=auth_headers, json=payload)

    res_get = client.get("/products", headers=auth_headers)
    assert res_get.status_code == 200
    assert res_get.get_json()["message"] == "Products retrieved successfully"
    products = res_get.get_json()["data"]["products"]
    assert len(products) >= 1


def test_get_products_empty(client, auth_headers):
    res_get = client.get("/products", headers=auth_headers)
    assert res_get.status_code == 200
    assert res_get.get_json()["message"] == "Products retrieved successfully"
    products = res_get.get_json()["data"]["products"]
    assert isinstance(products, list)


def test_get_products_error(client, monkeypatch, auth_headers):
    """Test exception during products list retrieval"""
    def _boom(*args, **kwargs):
        raise Exception("DB query error")
    monkeypatch.setattr("app.db.session.query", _boom)

    resp = client.get("/products", headers=auth_headers)
    assert resp.status_code == 500
    assert resp.json["success"] is False
    assert "Error fetching products" in resp.json["message"]


def test_get_product_by_id(client, auth_headers):
    payload = product_payload()
    res_post = client.post("/products", headers=auth_headers, json=payload)
    created_product = res_post.get_json()["data"]["product"]
    product_id = created_product["id"]

    res_get = client.get(f"/products/{product_id}", headers=auth_headers)
    assert res_get.status_code == 200
    assert res_get.get_json()["message"] == "Product retrieved successfully"
    fetched_product = res_get.get_json()["data"]["product"]
    assert fetched_product["id"] == product_id
    for key in payload:
        assert fetched_product[key] == payload[key]


def test_get_product_by_id_not_found(client, auth_headers):
    non_existent_id = str(uuid4())
    res_get = client.get(f"/products/{non_existent_id}", headers=auth_headers)
    assert res_get.status_code == 404
    assert res_get.get_json()["message"] == "Product not found"


def test_get_archived_product_by_id_not_found(client, auth_headers):
    """Test that archived products cannot be retrieved by ID"""
    payload = product_payload()
    res_post = client.post("/products", headers=auth_headers, json=payload)
    product_id = res_post.get_json()["data"]["product"]["id"]
    
    # Archive the product
    client.delete(f"/products/{product_id}", headers=auth_headers)
    
    # Should not be retrievable by ID when archived
    res_get = client.get(f"/products/{product_id}", headers=auth_headers)
    assert res_get.status_code == 404
    assert res_get.get_json()["message"] == "Product not found"


def test_get_product_by_id_error(client, monkeypatch, auth_headers):
    """Test exception during product retrieval"""
    def _boom(*args, **kwargs):
        raise Exception("DB query error")
    monkeypatch.setattr("app.db.session.query", _boom)

    resp = client.get(f"/products/{str(uuid4())}", headers=auth_headers)
    assert resp.status_code == 500
    assert resp.json["success"] is False
    assert "Error getting product" in resp.json["message"]


def test_update_patch_product(client, auth_headers):
    payload = product_payload()
    res_post = client.post("/products", headers=auth_headers, json=payload)
    created_product = res_post.get_json()["data"]["product"]
    product_id = created_product["id"]

    patch_payload = {
        "description": "Partially updated description."
    }
    res_patch = client.patch(f"/products/{product_id}", headers=auth_headers, json=patch_payload)
    assert res_patch.status_code == 200
    assert res_patch.get_json()["message"] == "Product updated successfully"
    updated_product = res_patch.get_json()["data"]["product"]
    assert updated_product["api_name"] == payload["api_name"]
    assert updated_product["description"] == patch_payload["description"]


def test_update_patch_product_validation_error(client, auth_headers):
    payload = product_payload()
    res_post = client.post("/products", headers=auth_headers, json=payload)
    product_id = res_post.get_json()["data"]["product"]["id"]

    patch_payload = {
        "api_name": "TestFailProduct"
    }
    res_patch = client.patch(f"/products/{product_id}", headers=auth_headers, json=patch_payload)
    assert res_patch.status_code == 400
    assert res_patch.get_json()["message"] == "Validation Error"


def test_update_patch_product_not_found(client, auth_headers):
    non_existent_id = str(uuid4())
    patch_payload = {"description": "Updated"}
    res_patch = client.patch(f"/products/{non_existent_id}", headers=auth_headers, json=patch_payload)
    assert res_patch.status_code == 404
    assert res_patch.get_json()["message"] == "Product not found"


def test_update_patch_archived_product(client, auth_headers):
    """Test that archived products cannot be updated"""
    payload = product_payload()
    res_post = client.post("/products", headers=auth_headers, json=payload)
    product_id = res_post.get_json()["data"]["product"]["id"]

    client.delete(f"/products/{product_id}", headers=auth_headers)

    res_patch = client.patch(f"/products/{product_id}", headers=auth_headers, json={"description": "New"})
    assert res_patch.status_code == 400
    assert "Cannot update an archived product" in res_patch.get_json()["message"]


def test_update_patch_product_db_error(client, monkeypatch, auth_headers):
    """Test database error during product PATCH update"""
    payload = product_payload()
    res_post = client.post("/products", headers=auth_headers, json=payload)
    product_id = res_post.get_json()["data"]["product"]["id"]

    def _boom():
        raise Exception("DB failure")
    monkeypatch.setattr("app.db.session.commit", _boom)

    resp = client.patch(f"/products/{product_id}", headers=auth_headers, json={"description": "Updated"})
    assert resp.status_code == 500
    assert resp.json["success"] is False
    assert "Error updating product" in resp.json["message"]


def test_update_put_product(client, auth_headers):
    payload = product_payload()
    res_post = client.post("/products", headers=auth_headers, json=payload)
    created_product = res_post.get_json()["data"]["product"]
    product_id = created_product["id"]

    put_payload = {
        "api_name": "Updated API Name",
        "description": "Updated description."
    }
    res_put = client.put(f"/products/{product_id}", headers=auth_headers, json=put_payload)
    assert res_put.status_code == 200
    assert res_put.get_json()["message"] == "Product updated successfully"
    updated_product = res_put.get_json()["data"]["product"]
    assert updated_product["api_name"] == put_payload["api_name"]
    assert updated_product["description"] == put_payload["description"]


def test_update_put_product_validation_error(client, auth_headers):
    payload = product_payload()
    res_post = client.post("/products", headers=auth_headers, json=payload)
    product_id = res_post.get_json()["data"]["product"]["id"]

    put_payload = {
        "api_name": "TestFailProduct",
        "description": "Updated"
    }
    res_put = client.put(f"/products/{product_id}", headers=auth_headers, json=put_payload)
    assert res_put.status_code == 400
    assert res_put.get_json()["message"] == "Validation Error"


def test_update_put_product_not_found(client, auth_headers):
    non_existent_id = str(uuid4())
    put_payload = {
        "api_name": "Updated API",
        "description": "Updated"
    }
    res_put = client.put(f"/products/{non_existent_id}", headers=auth_headers, json=put_payload)
    assert res_put.status_code == 404
    assert res_put.get_json()["message"] == "Product not found"


def test_update_put_archived_product(client, auth_headers):
    """Test that archived products cannot be updated via PUT"""
    payload = product_payload()
    res_post = client.post("/products", headers=auth_headers, json=payload)
    product_id = res_post.get_json()["data"]["product"]["id"]

    client.delete(f"/products/{product_id}", headers=auth_headers)

    res_put = client.put(f"/products/{product_id}", headers=auth_headers, json={
        "api_name": "NewName",
        "description": "NewDesc"
    })
    assert res_put.status_code == 400
    assert "Cannot update an archived product" in res_put.get_json()["message"]


def test_update_put_product_db_error(client, monkeypatch, auth_headers):
    """Test database error during product PUT update"""
    payload = product_payload()
    res_post = client.post("/products", headers=auth_headers, json=payload)
    product_id = res_post.get_json()["data"]["product"]["id"]

    def _boom():
        raise Exception("DB failure")
    monkeypatch.setattr("app.db.session.commit", _boom)

    resp = client.put(f"/products/{product_id}", headers=auth_headers, json={
        "api_name": "Updated",
        "description": "Updated"
    })
    assert resp.status_code == 500
    assert resp.json["success"] is False
    assert "Error updating product" in resp.json["message"]


def test_delete_product(client, auth_headers):
    payload = product_payload()
    res_post = client.post("/products", headers=auth_headers, json=payload)
    created_product = res_post.get_json()["data"]["product"]
    product_id = created_product["id"]

    res_delete = client.delete(f"/products/{product_id}", headers=auth_headers)
    assert res_delete.status_code == 200
    assert res_delete.get_json()["message"] == "Product has been archived successfully"
    archived_product = res_delete.get_json()["data"]["product"]
    assert archived_product["is_archived"] is True


    res_get = client.get("/products", headers=auth_headers)
    assert res_get.status_code == 200
    products = res_get.get_json()["data"]["products"]
    product_ids = [p["id"] for p in products]
    assert product_id not in product_ids


def test_delete_product_not_found(client, auth_headers):
    non_existent_id = str(uuid4())
    res_delete = client.delete(f"/products/{non_existent_id}", headers=auth_headers)
    assert res_delete.status_code == 404
    assert res_delete.get_json()["message"] == "Product not found"


def test_delete_product_db_error(client, monkeypatch, auth_headers):
    """Test database error during product deletion"""
    payload = product_payload()
    res_post = client.post("/products", headers=auth_headers, json=payload)
    product_id = res_post.get_json()["data"]["product"]["id"]

    def _boom():
        raise Exception("DB failure")
    monkeypatch.setattr("app.db.session.commit", _boom)

    resp = client.delete(f"/products/{product_id}", headers=auth_headers)
    assert resp.status_code == 500
    assert resp.json["success"] is False
    assert "Error archiving product" in resp.json["message"]


def test_product_contracts_empty(client, auth_headers):
    """Test retrieving contracts for a product with no subscriptions"""
    payload = product_payload()
    res_post = client.post("/products", headers=auth_headers, json=payload)
    product_id = res_post.get_json()["data"]["product"]["id"]

    res_get = client.get(f"/products/{product_id}/contracts", headers=auth_headers)
    assert res_get.status_code == 200
    assert res_get.get_json()["message"] == "Contracts retrieved successfully"
    contracts = res_get.get_json()["data"]["contracts"]
    assert isinstance(contracts, list)
    assert len(contracts) == 0


def test_product_contracts_with_single_subscription(client, auth_headers):
    """Test retrieving contracts for product with one subscription
    Covers: for subscription in product.subscriptions: cont = subscription.contract"""
    deps = create_subscription_dependencies(client, auth_headers)
    product_id = deps["product"]["id"]
    contract_id = deps["contract"]["id"]
    
    # Create subscription linking product to contract
    sub = create_subscription_using_api(client, auth_headers, contract_id, product_id)
    assert sub is not None, "Subscription creation failed"
    
    res_get = client.get(f"/products/{product_id}/contracts", headers=auth_headers)
    assert res_get.status_code == 200, f"Expected 200, got {res_get.status_code}: {res_get.get_json()}"
    assert res_get.get_json()["message"] == "Contracts retrieved successfully"
    contracts = res_get.get_json()["data"]["contracts"]
    assert len(contracts) == 1, f"Expected 1 contract, got {len(contracts)}: {contracts}"
    assert contracts[0]["id"] == contract_id


def test_product_contracts_with_multiple_subscriptions_same_contract(client, auth_headers):
    """Test that duplicate contracts are not returned (cont.id not in contracts_map deduplication)
    Covers: if cont and cont.id not in contracts_map: contracts_map[cont.id] = cont"""
    deps = create_subscription_dependencies(client, auth_headers)
    product_id = deps["product"]["id"]
    contract_id = deps["contract"]["id"]
    
    # Create two subscriptions for same product/contract combination
    sub1 = create_subscription_using_api(client, auth_headers, contract_id, product_id)
    sub2 = create_subscription_using_api(client, auth_headers, contract_id, product_id)
    assert sub1 is not None and sub2 is not None, "Subscription creation failed"
    
    res_get = client.get(f"/products/{product_id}/contracts", headers=auth_headers)
    assert res_get.status_code == 200, f"Expected 200, got {res_get.status_code}: {res_get.get_json()}"
    contracts = res_get.get_json()["data"]["contracts"]
    # Should only have 1 contract, not 2 (deduplication via contracts_map works)
    assert len(contracts) == 1, f"Expected 1 contract (deduplicated), got {len(contracts)}: {[c['id'] for c in contracts]}"
    assert contracts[0]["id"] == contract_id


def test_product_contracts_not_found(client, auth_headers):
    """Test retrieving contracts for non-existent product"""
    non_existent_id = str(uuid4())
    res_get = client.get(f"/products/{non_existent_id}/contracts", headers=auth_headers)
    assert res_get.status_code == 404
    assert res_get.get_json()["message"] == "Product not found"


def test_product_contracts_error(client, monkeypatch, auth_headers):
    """Test exception during product contracts retrieval"""
    payload = product_payload()
    res_post = client.post("/products", headers=auth_headers, json=payload)
    product_id = res_post.get_json()["data"]["product"]["id"]

    def _boom(*args, **kwargs):
        raise Exception("DB query error")
    monkeypatch.setattr("app.db.session.get", _boom)

    resp = client.get(f"/products/{product_id}/contracts", headers=auth_headers)
    assert resp.status_code == 500
    assert resp.json["success"] is False
    assert "Error getting contracts" in resp.json["message"]