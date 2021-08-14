from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "<body style = 'background-color: black'><br><h2 style='color: rgb(0,0,256)'><center>bot online</center></h2></body>"
    

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
    print("\033[0;36;48m * Webserver online")