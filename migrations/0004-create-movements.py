from yoyo import step

step("""
CREATE TABLE movements (
  id     SERIAL,
  token  VARCHAR,
  amount BIGINT
);
    """,
    """DROP TABLE movements;""")
