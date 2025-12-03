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
    """Creates a test user, generates a JWT token for them, and monkeypatches blueprints
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

    return token


@pytest.fixture
def auth_headers(savedToken):
    return {"Authorization": f"Bearer {savedToken}"}


@pytest.fixture(autouse=True)
def URL_to_uuid(app):
    """Wrap specific view functions so any 'id' kwarg that is a string
    is converted to a uuid.UUID before the view runs."""
    endpoints_to_patch = [
        "client.Client_id",
        "client.Client_Contracts_id",
        "subscription.Subscription_id",
        "subscription.Subscription_Tiers_id",
        "subscription_tier.Subscription_tier_id",
        "subscription_tier.Subscription_tier_Subscriptions_id",
        "contract.Contract_id",
        "contract.Contract_Product_id",
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

    # restore originals
    for endpoint, orig in originals.items():
        app.view_functions[endpoint] = orig


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