class Authentication(object):
    def __init__(self, db):
        self.db = db

    def valid_api_key(self, api_key):
        cursor = self.db.cursor()
        cursor.execute(
            """SELECT * FROM api_keys WHERE key = %s""",
            [api_key])

        return (cursor.rowcount == 1)

    def add_api_key(self, api_key):
        cursor = self.db.cursor()
        cursor.execute(
            """
                INSERT INTO api_keys (key)
                SELECT %s
                WHERE NOT EXISTS (SELECT 1 FROM api_keys WHERE key = %s);""",
            [api_key, api_key])

        self.db.commit()
