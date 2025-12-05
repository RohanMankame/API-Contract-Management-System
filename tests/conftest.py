# tests/conftest.py
import uuid
import pytest
from app import create_app, db as _db
from models.user import User
from flask_jwt_extended import create_access_token

@pytest.fixture
def app(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret")
    app = create_app()
    app.config["TESTING"] = True
    yield app


@pytest.fixture(autouse=True)
def clean_db(app):
    with app.app_context():
        _db.session.remove()
        _db.drop_all()
        _db.create_all()
    yield
    with app.app_context():
        _db.session.remove()
        _db.drop_all()

@pytest.fixture
def saved_token(app):
    with app.app_context():
        user = User(email=f"testuser-{uuid.uuid4().hex}@example.com", full_name="Test User")
        user.set_password("pass12345")
        _db.session.add(user)
        _db.session.commit()
        token = create_access_token(identity=str(user.id))
    return token


@pytest.fixture
def auth_headers(saved_token):
    return {"Authorization": f"Bearer {saved_token}"}

