import random
import json

async def addDataU(uid):
  
  user = await getDataU()
  if str(uid) in user:
    return False
  else:
    user[str(uid)] = {}
    user[str(uid)]["color"] = 'ffff00'
    user[str(uid)]["familyFriendly"] = 0
    user[str(uid)]["sniped"] = 1
    user[str(uid)]["dmblocker"] = 0

  with open("./json/userSettings.json","w") as f:
    json.dump(user,f)
  return True

async def getDataU():
  with open("./json/userSettings.json","r") as f:
    users = json.load(f)
  return users

async def addData(guildId):
  
  guilds = await getData()
  if str(guildId) in guilds:
    return False
  else:
    
    guilds[str(guildId)] = {}
    guilds[str(guildId)]["Nword"] = 0
    guilds[str(guildId)]["Fword"] = 0
    guilds[str(guildId)]["Cword"] = 0
    guilds[str(guildId)]["Prefix"] = '$'
    
    

  with open("./json/serverData.json","w") as f:
    json.dump(guilds,f)
  return True

async def getData():
  with open("./json/serverData.json","r") as f:
    guilds = json.load(f)
  return guilds

async def colorSetup(uid):
  
  await addDataU(uid)
  users = await getDataU()
  color = users[str(uid)]["color"]
  return color


async def changeff(string):
  string = string.replace("fuck", "f**k")
  string = string.replace("bitch", "bi**h")
  string = string.replace("shit", "sh*t")
  string = string.replace("ass", "a**")
  string = string.replace("bastard", "b*stard")
  string = string.replace("dick", "d**k")
  string = string.replace("penis","pp")
  string = string.replace("vagina","vag*na")
  return string
  


async def familyFriendlySetup(uid):
  await addDataU(uid)
  users = await getDataU()
  state = users[str(uid)]["familyFriendly"]
  
  if state == 1:
    return True
  if state == 0:
    return False




async def addDataSnipe(uid):
  
  user = await getDataSnipe()
  if str(uid) in user:
    return False
  else:
    user[str(uid)] = {}
    user[str(uid)]["deletedMessage"] = ''
    user[str(uid)]["date"] = ''
    user[str(uid)]["nsfw"] = False 
    


  with open("./json/userSnipeCache.json","w") as f:
    json.dump(user,f)
  return True

async def getDataSnipe():
  with open("./json/userSnipeCache.json","r") as f:
    users = json.load(f)
  
  return users



def getDataUpvote():
  with open("./json/upvoteData.json","r") as f:
    users = json.load(f)
  return users


  
def postTips():
    tips = [
      "If you encounter any errors, you may join the support server here.\nhttps://discord.gg/UCGAuRXmBD",
      "Support the bot by upvoting on top.gg!\nhttps://top.gg/bot/84475719231353652!",
      "Find the latest patch notes with the command ``$patchnotes``!",
      "Feeling bored? Troll your friends with all the commands in the 'troll' category! ",
      "You can change your preferred embed colour with ``$settings color [preferred color]``!",
      "Enabling ``$autoresponse`` will make the bot respond in a certain way to some words!",
      "Check the bot's ping with ``$ping``.",
      "Play a few fun games with your friend with the commands in the 'games' category!",
      "Try pinging the bot multiple times! They won't like it though...",
      "Getting destroyed in chat? Use ``$roast`` to crush their argument!"
      "Don't want to be DMed? Use ``$settings dmblocker on``!"
      "Find creative curse words with ``$swear``!"
      "Find some good memes on reddit with ``$meme``!"
      ]
    randomchance = random.randint(0,8)
    
    randomMsg = tips[random.randint(0,len(tips)-1)]
    if randomchance == 0:
      return f"**Tip:** {randomMsg}"
    else:
      return None
      
      
      
      
class egg:
  def __init__(self,id,egg1):
    self.id = id
    self.egg1 = egg1
    
  def write(self):
    with open("./json/egg.json","r") as f:
      user = json.load(f)
    
    if str(self.id) not in user:
      user[self.id] = {}
      user[self.id][self.egg1] = 0 
    
    with open("./json/egg.json","w") as f:
      json.dump(user,f)
    