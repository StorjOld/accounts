# -*- coding: utf-8 -*-
import pytest

from accounts.authentication import Authentication

# Database migrations run for each test in this module.
# See `conftest.pytest_runtest*`.
DB_MIGRATIONS = ['0006-create-api-keys']

# Fixtures ###

@pytest.fixture
def auth(db):
    return Authentication(db.connection)

# Tests ###

def test_add_api_key(db, auth):
    key = 'test'
    auth.add_api_key(key)
    db.execute("SELECT true FROM api_keys WHERE key = %s", [key])
    assert db.fetchone()[0] is True

def test_valid_api_key(db, auth):
    key = 'test'
    db.execute("INSERT INTO api_keys VALUES (1, %s)", [key])
    db.connection.commit()
    assert auth.valid_api_key(key) is True
