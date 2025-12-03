
def test_auth(client, savedToken):
    res = client.get("/protected", headers={"Authorization": f"Bearer {savedToken}"})
    print("Token is: " + savedToken)
    assert res.status_code == 200