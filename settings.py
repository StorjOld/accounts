
DATABASE_PATH = "dbname=storj user=storj password=so-secret host=localhost"

try:
    from local_settings import *
except ImportError:
    pass
