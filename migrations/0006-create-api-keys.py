from yoyo import step

step("""
CREATE TABLE api_keys (
  id  SERIAL,
  key VARCHAR
);
    """,
    """DROP TABLE api_keys;""")
