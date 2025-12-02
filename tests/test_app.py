from app import db
from models.user import User

def test_login(client, app):
    with app.app_context():
        user = User(email="rohan@gmail.com", full_name="Rohan")
        user.set_password("pass12345")
        db.session.add(user)
        db.session.commit()

   
    response = client.post('/login', json={"email": "rohan@gmail.com", "password": "pass12345"})
    assert response.status_code == 200
    assert "access_token" in response.json



"""
def test_add_user(client):
    response = client.post('/users', json={"username": "test"})
    assert response.status_code == 201
    assert response.json == {"message": "User created"}
"""