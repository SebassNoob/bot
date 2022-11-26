
from other.sqliteDB import get_db_connection, create_db
import typing
from typing import Any, List, Dict, Union

def insert(data : Dict[str, Any]) -> None:
  conn = get_db_connection("./other/serverSettings.db")
  #data looks like:
  '''
  data = {
    "id" : ... int,
    "autoresponse": ... int (bool),
    "autoresponse_content": ... str (dict),
    "blacklist": ... str (list)
  }
  
  '''
  
  conn.execute('INSERT INTO serverSettings (id, autoresponse, autoresponse_content, blacklist) VALUES (?,?,?,?)', (data.get('id'), data.get('autoresponse'), data.get('autoresponse_content'), data.get('blacklist')))

  conn.commit()
  conn.close()

def update(id: int, data : Dict[str, Any]) -> None:
  conn = get_db_connection("./other/serverSettings.db")
  #data looks like:
  '''
  data = {
    "autoresponse": ... int (bool),
    "autoresponse_content": ... str (dict),
    "blacklist": ... str (list)
  }
  
  '''
  
  conn.execute('UPDATE serverSettings SET (autoresponse, autoresponse_content, blacklist) =(?,?,?) WHERE id = (?)', ( data.get('autoresponse'), 
 data.get('autoresponse_content'), data.get('blacklist'), id))

  conn.commit()
  conn.close()
  

def delete(id: int) -> None:

  conn = get_db_connection("./other/serverSettings.db")
  
  
  conn.execute('DELETE FROM serverSettings WHERE id = (?)', (id, ))

  conn.commit()
  conn.close()

  
def get(id: int) -> Union[Dict[str, Any], None] :
  conn = get_db_connection("./other/serverSettings.db")
  
  
  data = conn.execute('SELECT * FROM serverSettings WHERE id = (?)', (id, )).fetchone()
  
  #data looks like:
  '''
  data = {
    "autoresponse": ... int (bool),
    "autoresponse_content": ... str (dict),
    "blacklist": ... str (list)
  }
  
  '''
  
  conn.close()
  return dict(data) if data is not None else None

  

