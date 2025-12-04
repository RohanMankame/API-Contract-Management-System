import uuid
import functools
from uuid import UUID

import pytest
from app import create_app, db as _db
from models.user import User
from flask_jwt_extended import create_access_token

@pytest.fixture
def app(monkeypatch):
    # use an ephemeral SQLite DB for tests
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret")
    app = create_app()
    app.config["TESTING"] = True
    # Do NOT call create_all() here; clean_db will manage schema creation
    yield app

@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def savedToken(client, app, monkeypatch):
    """
    Creates a test user, generates a JWT token for them, and monkeypatches blueprints
    so get_jwt_identity() returns a uuid.UUID object (test-only).
    """
    email = f"testuser-{uuid.uuid4().hex}@example.com"

    with app.app_context():

        User.query.filter_by(email=email).delete()
        _db.session.commit()

        user = User(email=email, full_name="Test User")
        user.set_password("pass12345")
        _db.session.add(user)
        _db.session.commit()

        user_id = user.id

    token = create_access_token(identity=str(user_id))   
    uuid_identity = uuid.UUID(str(user_id))
    monkeypatch.setattr("blueprints.auth.get_jwt_identity", lambda: uuid_identity)
    monkeypatch.setattr("blueprints.client.get_jwt_identity", lambda: uuid_identity)
    monkeypatch.setattr("blueprints.user.get_jwt_identity", lambda: uuid_identity)
    monkeypatch.setattr("blueprints.subscription.get_jwt_identity", lambda: uuid_identity)
    monkeypatch.setattr("blueprints.subscription_tier.get_jwt_identity", lambda: uuid_identity)
    monkeypatch.setattr("blueprints.contract.get_jwt_identity", lambda: uuid_identity)
    monkeypatch.setattr("blueprints.product.get_jwt_identity", lambda: uuid_identity)  

    return token


@pytest.fixture
def auth_headers(savedToken):
    return {"Authorization": f"Bearer {savedToken}"}


@pytest.fixture(autouse=True)
def clean_db(app):
    """Ensure DB schema is dropped and recreated for every test (function scope)."""
    with app.app_context():
        _db.session.remove()
        _db.drop_all()
        _db.create_all()
    yield
    with app.app_context():
        _db.session.remove()
        _db.drop_all()