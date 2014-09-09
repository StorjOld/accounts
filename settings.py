
DATABASE_PATH = "postgres://storj:so-secret@localhost/storj"
TEST_DB_PATH  = "postgres://postgres:postgres@localhost/storj_accounts_test"

try:
    from local_settings import *
except ImportError:
    pass
