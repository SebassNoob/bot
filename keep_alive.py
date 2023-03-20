from flask import Flask
from threading import Thread
import random



PORT = random.randint(2000,9000)
#test out diff ports
app = Flask('')

@app.route('/')
def home():
    return "on"
    

def run():
  app.run(host='0.0.0.0',port=PORT)
  

def keep_alive():  
      
    t = Thread(target=run)
    
    t.start()





