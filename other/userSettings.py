
from other.sqliteDB import get_db_connection, create_db
import typing
from typing import Any, List, Dict, Union

def insert(data : Dict[str, Any]) -> None:
  conn = get_db_connection("./other/userSettings.db")
  #data looks like:
  '''
  data = {
    "id" : ... int,
    "color": ... str,
    "familyFriendly": ... int (bool),
    "sniped": ... int (bool),
    "dmblocker": ... int (bool)
  }
  
  '''
  
  conn.execute('INSERT INTO userSettings (id, color, familyFriendly, sniped, dmblocker) VALUES (?,?,?,?,?)', (data.get('id'), data.get('color'), data.get('familyFriendly'), data.get('sniped'), data.get('dmblocker')))

  conn.commit()
  conn.close()

def update(id: int, data : Dict[str, Any]) -> None:
  conn = get_db_connection("./other/userSettings.db")
  #data looks like:
  '''
  data = {
    "color": ... str,
    "familyFriendly": ... int (bool),
    "sniped": ... int (bool),
    "dmblocker": ... int (bool)
  }
  
  '''
  
  conn.execute('UPDATE userSettings SET (color, familyFriendly, sniped, dmblocker) =(?,?,?,?) WHERE id = (?)', ( data.get('color'), data.get('familyFriendly'), data.get('sniped'), data.get('dmblocker'), id))

  conn.commit()
  conn.close()
  

def delete(id: int) -> None:

  conn = get_db_connection("./other/userSettings.db")
  
  
  conn.execute('DELETE FROM userSettings WHERE id = (?)', (id, ))

  conn.commit()
  conn.close()

  
def get(id: int) -> Union[Dict[str, Any], None] :
  conn = get_db_connection("./other/userSettings.db")
  
  
  data = conn.execute('SELECT * FROM userSettings WHERE id = (?)', (id, )).fetchone()
  
  
  conn.close()
  return dict(data) if data is not None else None

  



