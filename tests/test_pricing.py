# -*- coding: utf-8 -*-
import pytest

from accounts.pricing import Price, PriceDatabase

# Database migrations run for each test in this module.
# See `conftest.pytest_runtest*`.
DB_MIGRATIONS = ['0005-create-prices']

# Fixtures ###

@pytest.fixture
def price(db):
    return PriceDatabase(db.connection)

# Tests ###

def test_convert(price):
    res = price.convert((1, 20, 20))
    assert isinstance(res, Price)
    assert res.__dict__ == Price(20, 20).__dict__

def test_prices(db, price):
    db.execute("INSERT INTO prices (bytes, amount) VALUES (10, 10), (20, 20), (30, 30)")
    db.connection.commit()

    res = price.prices()
    assert len(res) == 3
    assert isinstance(res[0], Price)
    assert res[0].__dict__ == Price(10, 10).__dict__
