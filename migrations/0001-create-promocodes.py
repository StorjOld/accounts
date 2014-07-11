from yoyo import step

step("""
CREATE TABLE promocodes (
  id        SERIAL,
  promocode VARCHAR,
  bytes     BIGINT
);
    """,
    """DROP TABLE promocodes;""")
