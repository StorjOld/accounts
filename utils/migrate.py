import os

import psycopg2
import yoyo
import yoyo.connections

import settings

def path():
    return os.path.join(os.path.dirname(__file__), '..', 'migrations')

def run_migrations(dbconn=None, names=[]):
    if dbconn is None:
        dbconn, paramstyle = yoyo.connections.connect(settings.DATABASE_PATH)
    else:
        paramstyle = psycopg2.paramstyle

    migrations = yoyo.read_migrations(dbconn, paramstyle, path(), names=names)
    migrations.to_apply().apply()

    dbconn.commit()

if __name__ == '__main__':
    run_migrations()
