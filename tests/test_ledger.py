# -*- coding: utf-8 -*-
import pytest

from accounts.ledger import Ledger

# Database migrations run for each test in this module.
# See `conftest.pytest_runtest*`.
DB_MIGRATIONS = ['0003-create-balances', '0004-create-movements']

# Fixtures ###

@pytest.fixture
def ledger(db):
    return Ledger(db.connection)

# Tests ###

TOKEN = 'test'
AMOUNT = 100

def _get_balance(db, token):
    db.execute("SELECT amount FROM balances WHERE token = %s", [token])
    res = db.fetchone()
    return res and res[0]

def test_balance(db, ledger):
    assert ledger.balance(TOKEN) == 0

    db.execute("INSERT INTO balances (token, amount) VALUES (%s, %s)", [TOKEN, AMOUNT])
    db.connection.commit()
    assert ledger.balance(TOKEN) == AMOUNT

def test_deposit(db, ledger):
    # Account doesn't exist yet
    assert _get_balance(db, TOKEN) is None

    assert ledger.deposit(TOKEN, AMOUNT) is True
    assert _get_balance(db, TOKEN) == AMOUNT

    db.execute("SELECT amount FROM movements WHERE token = %s", [TOKEN])
    assert db.fetchone()[0] == AMOUNT

def test_withdraw(db, ledger):
    assert _get_balance(db, TOKEN) is None

    # Insufficient funds
    assert ledger.withdraw(TOKEN, AMOUNT) is False
    assert _get_balance(db, TOKEN) is None

    db.execute("INSERT INTO balances (token, amount) VALUES (%s, %s)", [TOKEN, AMOUNT+10])
    db.connection.commit()
    assert ledger.withdraw(TOKEN, AMOUNT) is True
    assert _get_balance(db, TOKEN) == 10

    db.execute("SELECT amount FROM movements WHERE token = %s", [TOKEN])
    assert db.fetchone()[0] == -AMOUNT
