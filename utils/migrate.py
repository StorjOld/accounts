import settings
import os

import yoyo
import yoyo.connections

def path():
    return os.path.join(os.path.dirname(__file__), 'migrations')

if __name__ == '__main__':
    conn, paramstyle = yoyo.connections.connect(settings.DATABASE_PATH)

    migrations = yoyo.read_migrations(conn, paramstyle, path())
    migrations.to_apply().apply()

    conn.commit()
