# -*- coding: utf-8 -*-
from collections import namedtuple
import json

import pytest

import index

# Fixtures ###

Price = namedtuple('Price', 'amount cost')
PRICES = [Price(a, c) for a, c in [(10, 10), (20, 20), (30, 30)]]

class MockManager(object):
    def __init__(self, dbpath):
        pass

    def generate(self):
        return 'test123'

    def prices(self):
        return PRICES

    def balance(self, token):
        return 50

    def redeem(self, token, promocode):
        return None if 'fail' in promocode else 20

    def valid_api_key(self, key):
        return False if not key or 'fail' in key else True

    def add(self, token, amount):
        return True

    def consume(self, token, amount):
        return False if not token or 'fail' in token else True

@pytest.fixture(autouse=True)
def patch_manager(monkeypatch):
    monkeypatch.setattr('accounts.Manager', MockManager)

@pytest.fixture(autouse=True)
def patch_flask():
    index.app.testing = True

@pytest.fixture
def app():
    return index.app.test_client()

# Dummy view for testing the authentication decorator
@index.app.route('/test-authentication', methods=['POST'])
@index.authenticate
def auth():
    return 'ok'


# Tests ###

def _decode_json(data):
    # json.loads() doesn't handle byte data in Python 3. -__-"
    # See http://bugs.python.org/issue10976.
    return json.loads(data.decode('utf-8'))

def test_authenticate(app):
    # No auth provided
    res = app.post('/test-authentication')
    assert res.status_code == 401
    assert _decode_json(res.get_data()) == {'status': 'invalid-authentication'}

    # Bad auth provided
    res = app.post('/test-authentication', headers=[('Authentication', 'failauth')])
    assert res.status_code == 401
    assert _decode_json(res.get_data()) == {'status': 'invalid-authentication'}

    # Successful auth
    res = app.post('/test-authentication', headers=[('Authentication', 'success')])
    assert res.status_code == 200
    assert res.get_data() == b'ok'

def test_account_manager():
    with index.app.app_context():
        assert isinstance(index.account_manager(), MockManager)

def test_token_new(app):
    res = app.post('/accounts/token/new')
    assert res.status_code == 200
    assert _decode_json(res.get_data()) == {'token': 'test123'}

def test_prices(app):
    res = app.get('/accounts/token/prices')
    assert res.status_code == 200
    assert _decode_json(res.get_data()) == {
            'prices': [
                {'amount': 10, 'cost': 10},
                {'amount': 20, 'cost': 20},
                {'amount': 30, 'cost': 30},
            ]
        }

def test_token_balance(app):
    res = app.get('/accounts/token/balance/testtoken')
    assert res.status_code == 200
    assert _decode_json(res.get_data()) == {'balance': 50}

def test_token_redeem(app):
    # No promocode specified
    res = app.post('/accounts/token/redeem/testtoken')
    assert res.status_code == 403
    assert _decode_json(res.get_data()) == {'status': 'error'}

    res = app.post('/accounts/token/redeem/testtoken',
            data='{"promocode": "testpromo"}',
            headers=[('Content-Type', 'application/json')])
    assert res.status_code == 201
    assert _decode_json(res.get_data()) == {'status': 'ok'}

def test_token_deposit(app):
    # No bytes provided
    res = app.post('/accounts/token/deposit/testtoken',
            headers=[('Authentication', 'testkey')])
    assert res.status_code == 400
    assert _decode_json(res.get_data()) == {'status': 'bad-request'}

    res = app.post('/accounts/token/deposit/testtoken', data='{"bytes": "30"}',
            headers=[('Content-Type', 'application/json'),
                    ('Authentication', 'testkey')])
    assert res.status_code == 200
    assert _decode_json(res.get_data()) == {'status': 'ok'}

def test_token_withdraw(app):
    # No bytes provided
    res = app.post('/accounts/token/withdraw/testtoken',
            headers=[('Authentication', 'testkey')])
    assert res.status_code == 400
    assert _decode_json(res.get_data()) == {'status': 'bad-request'}

    res = app.post('/accounts/token/withdraw/failtoken', data='{"bytes": "30"}',
            headers=[('Content-Type', 'application/json'),
                    ('Authentication', 'testkey')])
    assert res.status_code == 402
    assert _decode_json(res.get_data()) == {'error': 'balance-insufficient'}

    res = app.post('/accounts/token/withdraw/successtoken', data='{"bytes": "30"}',
            headers=[('Content-Type', 'application/json'),
                    ('Authentication', 'testkey')])
    assert res.status_code == 200
    assert _decode_json(res.get_data()) == {'status': 'ok'}

def test_coinbase_success(app):
    res = app.post('/accounts/coinbase/success/failkey/50')
    assert res.status_code == 401
    assert _decode_json(res.get_data()) == {'status': 'invalid-authentication'}

    res = app.post('/accounts/coinbase/success/testkey/50')
    assert res.status_code == 400
    assert _decode_json(res.get_data()) == {'status': 'bad-request'}

    res = app.post('/accounts/coinbase/success/testkey/50',
            data='{"order": {"custom": "testtoken"}}',
            headers=[('Content-Type', 'application/json')])
    assert res.status_code == 200
    assert _decode_json(res.get_data()) == {'status': 'ok'}
