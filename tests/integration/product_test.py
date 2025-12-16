from tests.factories import product_payload
from uuid import uuid4



def test_create_product(client, auth_headers):
    payload = product_payload()
    res_post = client.post("/products", headers=auth_headers, json=payload)

    assert res_post.status_code == 201
    assert res_post.get_json()["message"] == "Product created successfully"
    created_product = res_post.get_json()["data"]["product"]
    for key in payload:
        assert created_product[key] == payload[key]


def test_create_product_missing_fields(client, auth_headers):
    payload = {
        # "api_name" is missing
        "description": "A sample product description."
    }
    res_post = client.post("/products", headers=auth_headers, json=payload)

    assert res_post.status_code == 400


def test_create_product_invalid_fields(client, auth_headers):
    payload = {
        "api_name": 88,  # Invalid: empty string
        "description": "A sample product description."
    }
    res_post = client.post("/products", headers=auth_headers, json=payload)

    assert res_post.status_code == 400



def test_get_products(client, auth_headers):
    payload = product_payload()
    client.post("/products", headers=auth_headers, json=payload)

    res_get = client.get("/products", headers=auth_headers)
    assert res_get.status_code == 200
    assert res_get.get_json()["message"] == "Products retrieved successfully"
    products = res_get.get_json()["data"]["products"]
    assert len(products) >= 1



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
    updated_product_patch = res_patch.get_json()["data"]["product"]
    assert updated_product_patch["api_name"] == patch_payload.get("api_name", payload["api_name"])  
    assert updated_product_patch["description"] == patch_payload["description"]  




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
    updated_product_put = res_put.get_json()["data"]["product"]
    assert updated_product_put["api_name"] == put_payload["api_name"]
    assert updated_product_put["description"] == put_payload["description"]




def test_delete_product(client, auth_headers):
    payload = product_payload()
    res_post = client.post("/products", headers=auth_headers, json=payload)
    created_product = res_post.get_json()["data"]["product"]
    product_id = created_product["id"]

    res_delete = client.delete(f"/products/{product_id}", headers=auth_headers)
    assert res_delete.status_code == 200
    assert res_delete.get_json()["message"] == "Product has been archived successfully"

    res_get = client.get(f"/products/{product_id}", headers=auth_headers)
    assert res_get.status_code == 200
    fetched_product = res_get.get_json()["data"]["product"]
    assert fetched_product["id"] == product_id
    assert fetched_product["is_archived"] is True



def test_delete_product_not_found(client, auth_headers):
    non_existent_id = str(uuid4())
    res_delete = client.delete(f"/products/{non_existent_id}", headers=auth_headers)
    assert res_delete.status_code == 404
    assert res_delete.get_json()["message"] == "Product not found"


def test_cannot_update_archived_product(client, auth_headers):
    payload = product_payload()
    create = client.post("/products", headers=auth_headers, json=payload).get_json()["data"]["product"]
    pid = create["id"]
    client.delete(f"/products/{pid}", headers=auth_headers)

    res = client.patch(f"/products/{pid}", headers=auth_headers, json={"api_name": "newname"})
    assert res.status_code == 400
    assert "Cannot update an archived product" == res.get_json()["message"]
