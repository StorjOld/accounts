import psycopg2
import psycopg2.extras

def connect(*args, **kwargs):
    return connect_psycopg2(*args, **kwargs)

def connect_psycopg2(*args, **kwargs):
    db = psycopg2.connect(*args, **kwargs)

    db.cursor_factory = psycopg2.extras.DictCursor

    return db
