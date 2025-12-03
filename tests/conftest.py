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
    with app.app_context():
        _db.create_all()
    yield app
    with app.app_context():
        _db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def savedToken(client, app, monkeypatch):
    """Creates a test user, generates a JWT token for them, and patches"""

    email = f"Rohan@gmail.com"
    with app.app_context():
        User.query.filter_by(email=email).delete()
        _db.session.commit()
        user = User(email=email, full_name="Rohan Mankame")
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
    return token


@pytest.fixture
def auth_headers(savedToken):
    return {"Authorization": f"Bearer {savedToken}"}

import functools
from uuid import UUID
import pytest

@pytest.fixture(autouse=True)
def URL_to_uuid(app):
    endpoints_to_patch = [
    "client.Client_id",
    "client.Client_Contracts_id",
    "subscription.Subscription_id",
    "subscription.Subscription_Tiers_id",
]
    originals = {}
    for endpoint in endpoints_to_patch:
        orig = app.view_functions.get(endpoint)
        if not orig:
            continue
        originals[endpoint] = orig

        @functools.wraps(orig)
        def wrapper(*args, __orig__=orig, **kwargs):
            if "id" in kwargs and isinstance(kwargs["id"], str):
                try:
                    kwargs["id"] = UUID(kwargs["id"])
                except ValueError:
                    pass
            return __orig__(*args, **kwargs)

        app.view_functions[endpoint] = wrapper

    yield

    for endpoint, orig in originals.items():
        app.view_functions[endpoint] = orig


@pytest.fixture(autouse=True)
def clean_db(app):
    from app import db as _db
    with app.app_context():
        _db.session.remove()
        _db.drop_all()
        _db.create_all()
    yield
    with app.app_context():
        _db.session.remove()
        _db.drop_all()