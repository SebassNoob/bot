import json
import asyncio

import time



def upvoteCheck():
  while True:
    
    with open("./json/upvoteData.json","r") as f:
      file= json.load(f)
  
    for uid in list(file):
      file[uid] -= 1
      if file[uid] ==0:
        del file[uid]

      with open("./json/upvoteData.json", "w") as f:
        json.dump(file,f)
        f.close()

      
    time.sleep(60)

def getUserUpvoted():
  with open("./json/upvoteData.json","r") as f:
    file= json.load(f)
  d = list(file)
  return d
