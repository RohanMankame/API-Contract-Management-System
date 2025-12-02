from app import db
from models.client import Client

def test_create_client(client, auth_headers, app):
    with app.app_context():
        db.session.query(Client).delete()
        db.session.commit()

    client_data = {
        "company_name": "Test Client",  
        "email": "testclient@example.com",
        "phone_number" : "1234567890",
        "address": "123 Test St, Test City, TC 12345"
    }

    response = client.post('/Clients', json=client_data, headers=auth_headers)
    assert response.status_code == 201
    #assert response.get_json()["client"]["company_name"] == "Test Client"