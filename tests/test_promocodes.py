# -*- coding: utf-8 -*-
import pytest

from accounts.promocodes import PromocodeDatabase
from accounts.units import MEGABYTE

# Database migrations run for each test in this module.
# See `conftest.pytest_runtest*`.
DB_MIGRATIONS = ['0001-create-promocodes', '0002-create-promocode-uses']

# Fixtures ###

@pytest.fixture
def promo(db):
    return PromocodeDatabase(db.connection)

# Tests ###

TOKEN = 'test'
CODE = 'test'

def _get_promocode(db, code):
    db.execute("SELECT promocode FROM promocodes WHERE promocode = %s", [code])
    res = db.fetchone()
    return res and res[0]

def test_add_promocode(db, promo):
    assert _get_promocode(db, CODE) is None

    assert promo.add_promocode(CODE, MEGABYTE) is None
    assert _get_promocode(db, CODE) == 'test'

    # Don't add an existing promocode
    assert promo.add_promocode(CODE, MEGABYTE) is None
    assert _get_promocode(db, CODE) == 'test'

def test_redeem(db, promo):
    # Nonexistent promocode
    assert promo.redeem(TOKEN, CODE) is None

    # Add and redeem a promocode
    db.execute("INSERT INTO promocodes (promocode, bytes) VALUES (%s, %s)", [CODE, MEGABYTE])
    db.connection.commit()
    assert promo.redeem(TOKEN, CODE) == MEGABYTE
    db.execute("SELECT token FROM promocode_uses WHERE promocode = %s", [CODE])
    assert db.fetchone()[0] == TOKEN

    # Can't redeem an already used promocode
    assert promo.redeem(TOKEN, CODE) is None
