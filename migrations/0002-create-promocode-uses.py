from yoyo import step

step("""
CREATE TABLE promocode_uses (
  id        SERIAL,
  token     VARCHAR,
  promocode VARCHAR
);
    """,
    """DROP TABLE promocode_uses;""")
