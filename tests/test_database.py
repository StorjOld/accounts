# -*- coding: utf-8 -*-
import psycopg2
from psycopg2.extensions import STATUS_READY

import settings
from accounts.database import connect

def test_connect():
    con = connect(settings.TEST_DB_PATH)
    assert isinstance(con, psycopg2._psycopg.connection)
    assert con.status == STATUS_READY
    con.close()

def test_connect_fail():
    assert connect('') is None
