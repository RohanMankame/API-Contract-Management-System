
def test_auth(client, saved_token):
    res = client.get("/protected", headers={"Authorization": f"Bearer {saved_token}"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["logged_in_as"] is not None
    