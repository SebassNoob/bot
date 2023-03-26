import random
import json
import sqlite3
from other.sqliteDB import get_db_connection
import other.userSettings as userSettings 
import other.serverSettings as serverSettings 
from typing import *
import csv

def bool_to_int(bool):
  #although bad practice, this makes it readable
  if bool == True:
    return 1 
  elif bool == False:
    return 0 
  else:
    raise SyntaxError

    
def addDataU(uid: int) -> bool:
  if userSettings.get(uid) is None:
    userSettings.insert({
    "id" :uid,
    "color": "000000",
    "familyFriendly": bool_to_int(False),
    "sniped": bool_to_int(True),
    "dmblocker": bool_to_int(False)
    })
    
    return True
  else:
    
    return False
  
def getDataU(uid: int) -> Union[Dict[str, Any], None]:
  addDataU(uid)
  return userSettings.get(uid)

def addData(guildId: int) -> bool:
  with open("./json/autoresponse.csv",newline="") as file:
    reader = list(csv.DictReader(file))
    #reader is List[Dict[str, str]]
    #construct dict of shape Dict[str, str]
    autores = {i['word']: i['response'] for i in reader}
          
    
  if serverSettings.get(guildId) is None:
    serverSettings.insert({
    "id" :guildId,
    "autoresponse": 1,
    "autoresponse_content":f'{autores}',
    "blacklist": '[]'
    })
    
    return True
  else:
    
    return False


def getData(id: int) -> Union[Dict[str, Any], None]:
  
  return serverSettings.get(id)

  
def colorSetup(uid):
  
  addDataU(uid)
  
  
  return int(getDataU(uid).get('color'), 16)


def changeff(string: str) -> str:
  to_replace = {
    "fuck" :"f#k",
    "bitch": "bi##h",
    "shit": "sh#t",
    "ass": "a##",
    "bastard": "b#stard",
    "dick": "d##k",
    "penis": "pen#s",
    "vagina": "vag#na"
  }
  for old, new in to_replace.items():
    string = string.replace(old, new)
  
  return string
  



def getDataSnipe(uid):
  conn = get_db_connection("./other/snipe2.db")
  data = conn.execute("SELECT * FROM snipe WHERE id == (?)", (int(uid),)).fetchone()
  #returns (content, date, nsfw)
  if data:
    return (data[1],data[2],bool(data[3]))
  return None

def addDataSnipe(uid, message, date, nsfw=0):
  
  conn = get_db_connection("./other/snipe2.db")
  if getDataSnipe(uid) is not None:
    conn.execute("UPDATE snipe SET (deletedMessage, date, nsfw) = (?,?,?) WHERE id = (?)", (str(message),str(date),bool_to_int(nsfw),int(uid)))
    #TODO
  else:
    conn.execute("INSERT INTO snipe (id, deletedMessage, date,nsfw) VALUES (?,?,?,?)", (int(uid), str(message), str(date), bool_to_int(nsfw)))
  conn.commit()
  conn.close()






  
async def postTips(interaction):
    tips = [
      "If you encounter any errors, you may join the support server here.\nhttps://discord.gg/UCGAuRXmBD",
      "Support the bot by upvoting on top.gg!\nhttps://top.gg/bot/84475719231353652!",
      "Find the latest patch notes with the command ``/patchnotes``!",
      "Feeling bored? Troll your friends with all the commands in the 'troll' category! ",
      "You can change your preferred embed colour with ``/settings color [preferred color]``!",
      "Enabling ``/autoresponse`` will make the bot respond in a certain way to some words!",
      "Check the bot's ping with ``/ping``.",
      "Play a few fun games with your friend with the commands in the 'games' category!",
      "Try pinging the bot multiple times! They won't like it though...",
      "Getting destroyed in chat? Use ``/roast`` to crush their argument!",
      "Don't want to be DMed? Use ``/settings dmblocker on``!",
      "Annoy your friends in VCs with voice commands!",
      "Try our member/message commands! Right click on a message/member and navigate to apps to see the list.",
      "Find creative curse words with ``/swear``!",
      "Find some good memes on reddit with ``/meme``!",
      "If you see this, hope you're having a great day! 😉"
      ]
    #ez upvotes lol
    randomMsg = random.choice(tips)
    if random.randint(0,10) == 0:
      await interaction.channel.send(f"**Tip:** {randomMsg}")
      
      
    elif random.randint(0,20) == 0:
      await interaction.channel.send("**Tip:** Support the bot by upvoting on top.gg!\nhttps://top.gg/bot/84475719231353652!")
    
      
    
      
      
    