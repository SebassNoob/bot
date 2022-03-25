import sqlite3
#f'./other/data/{name}.db'
#'./other/schema.sql'
#f'./other/data/{name}.db'
def create_db(pathname_to_write, pathname_to_read):
  connection = sqlite3.connect(pathname_to_write)
  with open(pathname_to_read) as f:
    connection.executescript(f.read())

  connection.commit()
  connection.close()

def get_db_connection(pathname_to_read):
    conn = sqlite3.connect(pathname_to_read)
    conn.row_factory = sqlite3.Row
    return conn