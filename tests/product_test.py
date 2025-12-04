

def test_product(client, auth_headers):
    """
    Test creating a product and then retrieving it.
    """
    # POST
    post_res = client.post("/Products", headers=auth_headers, json={
        "api_name": "Open AI",
        "description": "AI LLM Service",
        })
    
    assert post_res.status_code == 201

    # GET
    get_res = client.get("/Products", headers=auth_headers)
    assert get_res.status_code == 200
    data = get_res.get_json()
    assert "products" in data

    product = data["products"][0]
    assert product["api_name"] == "Open AI"
    assert product["description"] == "AI LLM Service"


## for /Products/<id>
def test_product_by_id(client, auth_headers):
    """
    Test creating a product and then retrieving it by ID.  
    """
     # POST
    post_res = client.post("/Products", headers=auth_headers, json={
        "api_name": "Open AI Pro",
        "description": "Advanced AI LLM Service",
        })
    
    assert post_res.status_code == 201

    product_id = post_res.get_json()["product"]["id"]

    assert product_id is not None
    assert isinstance(product_id, str)

    # GET by ID
    get_res = client.get(f"/Products/{product_id}", headers=auth_headers)
    assert get_res.status_code == 200

    data = get_res.get_json()
    assert "product" in data
    product_data = data["product"]
    assert product_data["id"] == product_id