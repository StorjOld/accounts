from yoyo import step

step("""
CREATE TABLE prices (
  id     SERIAL,
  bytes  BIGINT,
  amount BIGINT
);
    """,
    """DROP TABLE prices;""")
