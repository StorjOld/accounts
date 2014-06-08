class Authentication(object):
    def __init__(self, db):
        self.db = db

    def valid_api_key(self, api_key):
        cursor = self.db.cursor()
        cursor.execute(
            """SELECT * FROM api_keys WHERE key = %s""",
            [api_key])

        return (cursor.rowcount == 1)
