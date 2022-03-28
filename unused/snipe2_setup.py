
#RUN IN SHELL - python3 unused/snipe2_setup.py
import sqlite3
def create_db(pathname_to_write, pathname_to_read):
  connection = sqlite3.connect(pathname_to_write)
  with open(pathname_to_read) as f:
    connection.executescript(f.read())

  connection.commit()
  connection.close()

create_db("./other/snipe2.db","./other/snipe2.sql")