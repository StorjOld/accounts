from yoyo import step

step("""
CREATE TABLE balances (
  id     SERIAL,
  token  VARCHAR,
  amount BIGINT
);
    """,
    """DROP TABLE balances;""")
