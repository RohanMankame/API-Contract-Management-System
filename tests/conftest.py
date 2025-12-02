# tests/conftest.py
import os
import pytest
from app import create_app, db as _db

@pytest.fixture
def app(tmp_path, monkeypatch):
    # Minimal test environment values
    monkeypatch.setenv('DATABASE_URL', 'sqlite:///:memory:')
    monkeypatch.setenv('JWT_SECRET_KEY', 'test-secret')

    # Create app using factory
    app = create_app()
    app.config['TESTING'] = True

    # Create db schema fresh for tests
    with app.app_context():
        _db.create_all()

    yield app

    # teardown: drop all
    with app.app_context():
        _db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()