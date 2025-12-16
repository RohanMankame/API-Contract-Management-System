
# Positive test
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



