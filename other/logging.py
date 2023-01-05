import sqlite3
from other.sqliteDB import get_db_connection

def log(cmd_name):
  conn = get_db_connection("./other/logging.db")

  
  data = conn.execute('SELECT * FROM logging WHERE cmd == (?) ', (cmd_name,)).fetchall()

  updated = int(data[0][1]) +1
  #gives updated numTimes
    
    
  
  if data == list():
    conn.execute('INSERT INTO logging (cmd,numTimes) VALUES (?,?)',(cmd_name,1))
  else:
    conn.execute('UPDATE logging SET numTimes = (?) WHERE cmd = (?)',(updated, cmd_name))
    
  conn.commit()
  conn.close()




