
from other.sqliteDB import get_db_connection
import time

def clearSnipe():

  while True:

    conn = get_db_connection("./other/snipe2.db")
    conn.execute('DELETE FROM snipe')
        
    
    conn.commit()
    conn.close()
    time.sleep(60*60*2)