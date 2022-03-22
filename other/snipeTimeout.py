import json
import datetime
import time
import base64

def snipeTimeout():
  
  
  
    
  while True:
    
    current_month = datetime.datetime.now().month
    with open("./other/snipeTimeout.json","r") as f:
      month = json.load(f)
  
    if month["month"] != current_month:
      
    
      
      month["month"] = current_month
      
      with open("./other/snipeTimeout.json","w") as f:
        json.dump(month,f)
        
      with open("./json/userSnipeCache.json","r") as f:
        cache = json.load(f)
      for key in cache:
        
        
        del key
      cache = {}
      
      with open("./json/userSnipeCache.json","w") as f:
        json.dump(cache,f)
        
    else:
      pass
  

def encodeCache():
  while True:
    
    with open("./json/userSnipeCache.json","rb") as f:
      data = json.load(f)
    keys = []
    for key in data:
      keys.append(key)
    
    for i in range(len(keys)):
      if data[keys[i]]["encoded"] == False:
        msg=str(data[keys[i]]["deletedMessage"])
        encrypt = base64.b64encode(msg.encode('utf-8',errors = 'strict'))
        
        e ={"deletedMessage":encrypt.decode('ascii'),"encoded":True}
        data[keys[i]].update(e)
        
        with open("./json/userSnipeCache.json","w") as f:
          
          json.dump(data,f)
          
      else:
        continue
    time.sleep(180)