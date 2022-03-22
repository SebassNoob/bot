import sqlite3

def create_db(name):
  connection = sqlite3.connect(f'./other/data/{name}.db')

  with open('./other/schema.sql') as f:
    connection.executescript(f.read())

  connection.commit()
  connection.close()

def get_db_connection(name):
    conn = sqlite3.connect(f'./other/data/{name}.db')
    conn.row_factory = sqlite3.Row
    return conn