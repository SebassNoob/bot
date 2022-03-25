from flask import Flask
from threading import Thread
import requests
import time
import logging
import random
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

PORT = random.randint(2000,9000) 
#test out diff ports
app = Flask('')

@app.route('/')
def home():
    return "<body style = 'background-color: black'><br><h2 style='color: rgb(0,0,256)'><center>bot online</center></h2></body>"
    

def run():
  app.run(host='0.0.0.0',port=PORT)
  
def ping(target, debug):
    while(True):
      session = requests.Session()
      retry = Retry(connect=2, backoff_factor=10)
      adapter = HTTPAdapter(max_retries=retry)
      session.mount('http://', adapter)
      session.mount('https://', adapter)

      
      try:
          
        r = session.get(target)
      except requests.exceptions.ConnectionError:
        pass
      if(debug == True):
        print(" * Ping Status Code: " + str(r.status_code))
      time.sleep(random.randint(180,300)) 

    
def keep_alive(debug=True):  
    log = logging.getLogger('werkzeug')
    log.disabled = True
    app.logger.disabled = True  
    t = Thread(target=run)
    r = Thread(target=ping, args=("https://bot.sebassnoob.repl.co/",debug,))
    t.start()
    r.start()




