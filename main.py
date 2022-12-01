
import os
import random
import discord
from other.asyncCmds import addData,colorSetup,getData,addDataSnipe,getDataSnipe, addDataU
from restart import run_main
from discord.ext import commands
from keep_alive import keep_alive
import datetime

import json


from other.upvoteExpiration import upvoteCheck
from threading import Thread
from other.asyncCmds import egg
import time
from other.snipeTimeout import clearSnipe
import sys
sys.path.insert(1,'./other')
import sqlite3
from sqliteDB import get_db_connection
from os import system
system("pip install spacy")
system("python -m spacy download en_core_web_sm")

import topgg


#methodology for updating

#commit changes in bot
#pull changes to bot-1
#write + test code in bot-1
#sysexit bot
#for all changed files in bot, copy and paste manually into bot-1
#commit to repo
#pull to bot
#run



def get_prefix(bot, message): 
  return '$'





#bot object here
class Bot(commands.AutoShardedBot):
  def __init__(self):
    intents = discord.Intents.default()
    intents.message_content = True
    
    super().__init__(command_prefix=get_prefix, intents=intents, shard_count= 2, help_command= None)

  async def on_ready(self):
    servers = len(self.guilds)
    print("\033[0;36;48m-----------------------------------------")
    print(f" * {self.user} connected to {servers} servers")
  
    count = {}
    for guild in self.guilds:
      addData(guild.id)
      
      if guild.shard_id not in count:
        count[guild.shard_id] = 1
      else:
        count[guild.shard_id] += 1
    for t in count.items():
    
      print(f"   - Shard {t[0]}: {t[1]} servers")
    print("\033[0;36;48m-----------------------------------------")
    await self.change_presence(activity=discord.Game(name=f"$help | annoying {servers} servers"))
    await self.tree.sync()
    return

  async def on_guild_join(self,guild):
    print(guild.name)
    addData(guild.id)
    for channel in guild.text_channels:
      if channel.permissions_for(guild.me).send_messages:
      
        em = discord.Embed(color = 0x000555,title="A very suitable welcome message", description = "Hey, annoybot here. My prefix is $, and if you need any help, visit the [support server](https://discord.gg/UCGAuRXmBD)!")
        em.set_footer(text = "The embodiment of discord anarchy")
        await channel.send(embed = em)
        break


  async def on_command_error(self,ctx, error):
  
  
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
    
      raise Exception("CommandNotFound")
    
    if isinstance(error, discord.ext.commands.MissingRequiredArgument):
        em = discord.Embed(color = 0x000000, description = f"You're missing an argument: ``{error.param}`` in that command, dumbass.")
        await ctx.reply(embed = em)
        raise Exception("MissingRequiredArgument")
        
    if isinstance(error,commands.CommandInvokeError):
    
      if str(error) == "Command raised an exception: NotFound: 404 Not Found (error code: 10008): Unknown Message":
        raise Exception("NotFound")

      elif error == "Command raised an exception: Forbidden: 403 Forbidden (error code: 50007): Cannot send messages to this user":
        await ctx.send(embed = discord.Embed(color = 0x000000, description = "This user most likely is a bot, or has blocked the bot. What a pussy."))
      elif str(error) == "Command raised an exception: ClientException: Already connected to a voice channel.":
        await ctx.send(embed = discord.Embed(color = 0x000000, description = "The bot is already connected to a voice channel, dumbass."))
      elif str(error).startswith("Command raised an exception: Exception:"):
        pass
      elif "Command raised an exception: NotFound: 404 Not Found (error code: 0): Interaction is unknown (you have already responded to the interaction or responding took too long)"  == str(error):
          pass
      elif "Command raised an exception: TimeoutError:" in str(error):
          pass
      elif str(error) == "Command raised an exception: NotFound: 404 Not Found (error code: 0): Interaction is unknown (you have already responded to the interaction or responding took too long)":
        pass
    
      elif "Command raised an exception: Exception:" in str(error):
        pass

      elif "Interaction is unknown" in str(error):
        pass
      else:
      
        em = discord.Embed(color = 0x000000,title = "Unknown error.", description = f"This has been reported to the [support server](https://discord.gg/UCGAuRXmBD). Please join and provide the context on what happened and how to reproduce it. \nFull traceback:\n```py\n{error}```")
        await ctx.send(embed = em)
        channel = self.get_channel(953214132058992670)
        await channel.send(embed=em)
        raise error
    if isinstance(error, commands.CommandOnCooldown):
      with open("./json/upvoteData.json","r") as f:
        data = json.load(f)
        
      if str(ctx.author.id) in data.keys():
        em = discord.Embed(color = 0x000000,description = 'This command is on a **%.1fs** cooldown.\nSince you upvoted in the past 12 hours or claimed your daily in the past 30 minutes, you get lower cooldowns!' % error.retry_after)
        
        await ctx.reply(embed= em)
        
        
      else:
        em = discord.Embed(color = 0x000000,description = 'This command is on a **%.1fs** cooldown. Upvote to get lower cooldowns [here](https://top.gg/bot/844757192313536522)!' % error.retry_after)
        
        await ctx.reply(embed= em)
      raise Exception("CommandOnCooldown")
    if isinstance(error, commands.MissingPermissions):
        em = discord.Embed(color = 0x000000, description = f"❌ You need the ``{error.missing_perms}`` permission to use that command.")
        await ctx.reply(embed = em)
        raise Exception("MissingPermissions")
    
    if isinstance(error, discord.ext.commands.errors.BotMissingPermissions):
        em = discord.Embed(color = 0x000000, description = f"❌ I don't have permissions for that! I need the {error.missing_perms} permission(s).")
        await ctx.send(embed = em)
        raise Exception("BotMissingPermissions")
    if isinstance(error, discord.ext.commands.errors.MemberNotFound):
        em = discord.Embed(color = 0x000000, description = "❌ The member you mentioned was not found, actually send a member name next time you moron.")
        await ctx.send(embed = em)
        raise Exception("MemberNotFound")



  

  async def on_message_delete(self,message):

  
      
    current_time = datetime.datetime.now() 

    addDataSnipe(message.author.id, message.content, current_time, message.channel.nsfw)
    
    
  
  
  

  async def on_interaction(self, interaction):
    addDataU(interaction.user.id)
    



  #ON_MESSAGE
  async def on_message(self,message):
    
    if message.author == self.user:
      return
    else:
      await self.process_commands(message)
    
    
    #autoresponse
    if not message.guild:
      return 
    
    conn = get_db_connection("./other/serverSettings.db")
  
  
    data = conn.execute('SELECT autoresponse, autoresponse_content FROM serverSettings WHERE id = (?)', (message.guild.id, )).fetchone()
      
    conn.close()
    if bool(dict(data)['autoresponse']) and message.content in eval(dict(data)['autoresponse_content']).keys():
      await message.channel.send(eval(dict(data)['autoresponse_content'])[message.content])
        
      
    
      
      if f'<@{self.user.id}>' in message.content or f'<@!{self.user.id}>' in message.content :
      
        if 'help' in message.content:
          em = discord.Embed(color = 0x000555,title="You need help? Get it yourself.", description = " My default prefix is $, and if you need any help, visit the [support server](https://discord.gg/UCGAuRXmBD)!")
          em.set_footer(text = "The embodiment of discord anarchy")
          await message.channel.send(embed = em)

      
                
        if 'invite' in message.content:
          await message.channel.send("here you go, you lazy ass.", components=[ 
              [
                  Button(
                      label = "invite",
                      url = "https://discord.com/api/oauth2/authorize?client_id=844757192313536522&permissions=4294967287&scope=bot",
                      style = 5
                      
                  )]])

        if 'prefix' in message.content:
          await message.channel.send(f"Your server uses: ``{get_prefix(self, message)}`` as the prefix for all bot commands.")  

        else:
          
          user = egg(message.author.id,0)
          user.write()
          with open("./json/egg.json","r") as f:
            hello = json.load(f)
        
          while True:
          
            if hello[str(user.id)]["0"] == 0:
            
              hello[str(user.id)]["0"]=1
            
              with open("./json/egg.json","w") as f:
                json.dump(hello,f)
              await message.channel.send("Stop pinging me.")
              break
            if hello[str(user.id)]["0"] == 1:
              hello[str(user.id)]["0"]=2
              with open("./json/egg.json","w") as f:
                json.dump(hello,f)
              await message.channel.send("I said, STOP PINGING ME YOU DUMB F**K")
              break
            if hello[str(user.id)]["0"] == 2:
              hello[str(user.id)]["0"]=3
              with open("./json/egg.json","w") as f:
                json.dump(hello,f)
              await message.channel.send("https://imgur.com/t/mike_wazowski/lQyLC5G")
              break
            if hello[str(user.id)]["0"] == 3:
              hello[str(user.id)]["0"]=4
              with open("./json/egg.json","w") as f:
                json.dump(hello,f)
              await message.channel.send("https://miro.medium.com/max/324/1*HI4kj-TPAQrfQkAdrw2KTA.png")
              break
            if hello[str(user.id)]["0"] == 4:
              hello[str(user.id)]["0"]=5
              with open("./json/egg.json","w") as f:
                json.dump(hello,f)
              await message.channel.send("https://memegenerator.net/img/instances/61640131.jpg")
              break
            if hello[str(user.id)]["0"] == 5:
              hello[str(user.id)]["0"]=0
              with open("./json/egg.json","w") as f:
                json.dump(hello,f)
              await message.channel.send("HOW WOULD YOU FEEL IF I PINGED YOU THEN")
              for i in range(5):
                await message.channel.send(f"<@!{message.author.id}>")
                time.sleep(1)
              break
          
          
          
          
        
    
    if message.channel.id == 864467615891324938 and "ty" in message.content and "for" in message.content and "upvoting" in message.content:
      data = message.content.split(" ")
      data = list(data)[1]
      data = str(data)[2:-1]

    
      with open("./json/upvoteData.json","r") as f:
        file= json.load(f)
    
      try:
        d = {data: file[data]+720}

        file.update(d)
      except KeyError:
        file[data] = 720
    
    
      with open("./json/upvoteData.json","w") as f:
        json.dump(file,f)
        f.close

  async def setup_hook(self):
    for filename in os.listdir('./cogs'):
      if filename.endswith('.py'):

    
        await bot.load_extension(f'cogs.{filename[:-3]}')
        print(f"\033[0;32;49m{filename} loaded")
      
    


      
    
  



bot = Bot()



  
  




















@bot.command()
async def patchnotes(ctx):
  color = int(await colorSetup(ctx.message.author.id),16)
  em = discord.Embed(color = color)
  em.add_field(name = "1.8.0 part I", value = "``**1.8.0 part I**\nThis serves as a bridging update for the future release of discord.py 2.0, as well as general updates to the bot.\n- ADD: proper error messages for common errors\n- FIX: iplookup failing in some cases\n- ADD: textwall command\n- CHANGE: snipe cache clear 30 days => 2 hours\n- CHANGE: snipe is now more reliable (database will not corrupt) but slightly slower\n- FIX: (hopefully) resolves poor uptime lately \n- CHANGE: Privacy policy got an update\n- ADD: more dark humor yay``",inline = False)
  await ctx.send(embed = em)







    







@bot.command()
async def servers(ctx):
  for server in bot.guilds:
    print(server.name, server.id)

  

@bot.command()
async def sysexit(ctx):
  
  if int(ctx.author.id) == int(os.getenv("uid")):
    await ctx.send("Bot has been taken offline.")
    sys.exit()

@bot.command()
async def restart(ctx):
  if int(ctx.author.id) == int(os.getenv("uid")):
    await ctx.send("Bot is restarting...")
    system("python restart.py")

    

Thread(target=upvoteCheck).start()
Thread(target=clearSnipe).start()

keep_alive() 

try:
    bot.run(os.getenv('TOKEN'))
except discord.errors.HTTPException as e:
  print(e) 
  print("restarting in 10s...")
  time.sleep(10)
  system("python restart.py")
    


