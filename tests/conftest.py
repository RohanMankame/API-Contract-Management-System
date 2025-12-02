# tests/conftest.py
import pytest
from app import create_app, db as _db

@pytest.fixture
def app(tmp_path, monkeypatch):
    # Keep tests self-contained: in-memory DB and a test JWT key
    monkeypatch.setenv('DATABASE_URL', 'sqlite:///:memory:')
    monkeypatch.setenv('JWT_SECRET_KEY', 'test-secret')

    app = create_app()
    app.config['TESTING'] = True

    with app.app_context():
        _db.create_all()

    yield app

    # teardown
    with app.app_context():
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_token(client, app):
    """
    Create a fresh test user and return a JWT access token.
    Safe and idempotent (cleans any existing test user).
    """
    from models.user import User

    with app.app_context():
        _db.session.query(User).delete()
        _db.session.commit()

        u = User(email="rohan@gmail.com", full_name="Rohan Mankame")
        u.set_password("pass12345")
        _db.session.add(u)
        _db.session.commit()

    resp = client.post('/login', json={"email": "rohan@gmail.com", "password": "pass12345"})
    assert resp.status_code == 200, f"login failed in fixture: {resp.status_code} {resp.get_data(as_text=True)}"
    return resp.json["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    """Return headers dict ready for use in test requests."""
    return {"Authorization": f"Bearer {auth_token}"}