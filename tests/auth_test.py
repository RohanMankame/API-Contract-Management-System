
def test_auth(client, savedToken):
    res = client.get("/protected", headers={"Authorization": f"Bearer {savedToken}"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["logged_in_as"] is not None
    