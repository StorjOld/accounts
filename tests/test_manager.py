# -*- coding: utf-8 -*-
from collections import namedtuple

import pytest

from accounts.manager import Manager

# Fixtures ###

Price = namedtuple('Price', 'amount cost')
PRICES = [Price(a, c) for a, c in [(10, 10), (20, 20), (30, 30)]]
TOKEN = 'test'

@pytest.fixture(autouse=True)
def patch_integrations(monkeypatch):
    def redeem(self, token, promo):
        return None if promo == 'nonexistent' else 20

    def withdraw(self, token, amount):
        return False if token == 'insufficient' else True

    monkeypatch.setattr('accounts.authentication.Authentication.add_api_key', lambda s, k: None)
    monkeypatch.setattr('accounts.authentication.Authentication.valid_api_key', lambda s, k: True)
    monkeypatch.setattr('accounts.generator.generate', lambda: 'test')
    monkeypatch.setattr('accounts.ledger.Ledger.deposit', lambda s, t, a: True)
    monkeypatch.setattr('accounts.ledger.Ledger.withdraw', withdraw)
    monkeypatch.setattr('accounts.ledger.Ledger.balance', lambda s, t: 50)
    monkeypatch.setattr('accounts.pricing.PriceDatabase.prices', lambda s: PRICES)
    monkeypatch.setattr('accounts.promocodes.PromocodeDatabase.redeem', redeem)
    monkeypatch.setattr('accounts.promocodes.PromocodeDatabase.add_promocode', lambda s, p, b: None)

@pytest.fixture
def manager(db):
    # The DB path is irrelevant since we're mocking out all integrations
    return Manager('')

# Tests ###

def test_generate(manager):
    assert manager.generate() == 'test'

def test_prices(manager):
    assert manager.prices() == PRICES

def test_redeem(manager):
    assert manager.redeem(TOKEN, 'nonexistent') is False
    assert manager.redeem(TOKEN, 'test') is True

def test_add_promocode(manager):
    assert manager.add_promocode('test', 20) is None

def test_balance(manager):
    assert manager.balance(TOKEN) == 50

def test_consume(manager):
    assert manager.consume('insufficient', 50) is False
    assert manager.consume(TOKEN, 50) is True

def test_can_consume(manager):
    assert manager.can_consume(TOKEN, 60) is False
    assert manager.consume(TOKEN, 50) is True

def test_add_api_key(manager):
    assert manager.add_api_key(TOKEN) is None

def test_valid_api_key(manager):
    assert manager.valid_api_key(TOKEN) is True
