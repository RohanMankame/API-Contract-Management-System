
from tests.factories import user_payload
import uuid


def test_login(client, auth_headers):
    payload = user_payload()
    res_post = client.post("/users", headers=auth_headers, json=payload)

    assert res_post.status_code == 201

    res_post = client.post("/login", json={
        "email": payload["email"],
        "password": payload["password"]
    })
    assert res_post.status_code == 200
    data = res_post.get_json()
    assert "token" in data["data"]



def test_auth(client, saved_token):
    res = client.get("/protected", headers={"Authorization": f"Bearer {saved_token}"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["data"]["email"] is not None
    
# Negative tests
def test_auth_no_jwt_token(client):
    res = client.get("/protected")
    assert res.status_code == 401 


def test_auth_invalid_jwt_token(client):
    res = client.get("/protected", headers={"Authorization": "Bearer ?|-RANDOM_INVALID_TOKEN-|?"})
    assert res.status_code == 422 



