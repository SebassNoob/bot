from dotenv import load_dotenv

load_dotenv()
import os
import random
import discord
from discord import app_commands
from cogs.misc import Misc
from other.utilities import addData,colorSetup,getData,addDataSnipe,getDataSnipe, addDataU, postTips
from logging.handlers import TimedRotatingFileHandler
import logging
from discord.ext import commands
from keep_alive import keep_alive
import datetime
import asyncio
import json
import traceback
from other.customCooldown import CustomCooldown

import threading
from threading import Thread
import time
from other.snipeTimeout import clearSnipe
import sys
sys.path.insert(1,'./other')
from sqliteDB import get_db_connection
from os import system
import collections




async def blacklist_check(interaction: discord.Interaction):
  if not interaction.guild:
    return True
  try:
    if interaction.user.id in eval(getData(interaction.guild.id)['blacklist']):
      em = discord.Embed(color = 0x000000, description = f"You have been banned from using this bot in this server: {interaction.guild.name}\nAsk the mods to unban you (/serversettings) or use this bot in another server.")
      await interaction.response.send_message(embed = em, ephemeral = True)
      return False
  except:
    addDataU(interaction.user.id)
    addData(interaction.guild.id)
    return True

  return True


#bot object here
class Bot(commands.AutoShardedBot):
  def __init__(self):
    intents = discord.Intents.default()
    intents.message_content = True
    
    super().__init__(command_prefix="a$", intents=intents, shard_count= 2, help_command= None)
    


  async def on_ready(self):
    servers = len(self.guilds)
    print("\033[0;36;48m-----------------------------------------")
    print(f"[INFO] * {self.user} connected to {servers} servers")
    
    count = collections.Counter([guild.shard_id for guild in self.guilds])
    
    
    for t in count.items():
    
      print(f"[INFO]   - Shard {t[0]}: {t[1]} servers")
    print("\033[0;36;48m-----------------------------------------")

    await self.change_presence(activity=discord.Game(name=f"/help | annoying {servers} servers"))

    

    for cmd in self.tree.walk_commands():
      
      cmd = app_commands.checks.dynamic_cooldown(CustomCooldown)(cmd)
      
      if not isinstance(cmd, app_commands.Group):
        cmd.add_check(blacklist_check)
        
      

    
    async def err_handler(interaction: discord.Interaction, error: app_commands.AppCommandError):


      
      
      
      if isinstance(error, app_commands.MissingPermissions):
        em = discord.Embed(color = 0x000000, description = f"❌ You need the ``{error.missing_permissions}`` permission to use that command.")
        await interaction.response.send_message(embed = em)
        return
      if isinstance(error, app_commands.BotMissingPermissions):
        em = discord.Embed(color = 0x000000, description = f"❌ I don't have permissions for that! I need the ``{error.missing_permissions}`` permission(s).")
        await interaction.response.send_message(embed = em)
        return
      if isinstance(error, app_commands.CommandOnCooldown):
        em = discord.Embed(color = 0x000000,description = "You have exceeded this command's ratelimits. Try again in **%.1fs** cooldown." % error.retry_after)
        
        
        await interaction.response.send_message(embed= em)
        return 
      
      if isinstance(error, discord.Forbidden):
        em = discord.Embed(color = 0x000000,description = f"The bot is missing permissions. Check /help to see the required permissions. If the problem persists, contact the [support server](https://discord.gg/UCGAuRXmBD)\nHTTP body:```{error.text}```")
        
        await interaction.response.send_message(embed= em)
        return
      else:
        
      
        em = discord.Embed(color = 0x000000,title = "Unknown error.", description = f"This has been reported to the [support server](https://discord.gg/UCGAuRXmBD). Please join and provide the context on what happened and how to reproduce it.\nCommand: {error.command.name if hasattr(error, 'command') else 'unknown'}\nFull traceback:\n```{error}```\nHTTP response code: ``{error.status if hasattr(error, 'status') else 'unknown'}``\nHTTP body:```{error.text if hasattr(error, 'text') else 'unknown'}```")
        await interaction.followup.send(embed = em)
        channel = self.get_channel(953214132058992670)
        logging.log(40, f"[ERROR] Command: {error.command.name if hasattr(error, 'command') else 'unknown'}\nFull traceback:\n{error}")
        await channel.send(embed=em)
        return



    
    self.tree.on_error = err_handler



    await self.tree.sync()
    return

  async def on_guild_join(self,guild):
    print(f'[INFO] joined {guild.name}: {guild.id}')
    addData(guild.id)
    for channel in guild.text_channels:
      if channel.permissions_for(guild.me).send_messages:
        with open('./json/welcome_message.txt', 'r') as w:
          em = discord.Embed(color = 0x000555,title="A very suitable welcome message", description = ''.join(w.readlines()))
        em.set_footer(text = "The embodiment of discord anarchy")
        await channel.send(embed = em)
        return
    #if there is no channel where the bot is allowed to send the welcome message in, ignore and log the server
    print('[WARNING] failed to send welcome to '+ guild.name)

  

  
  
  async def on_message_delete(self,message):

  
      
    current_time = datetime.datetime.now() 
    if isinstance(message.channel, discord.abc.GuildChannel):
      nsfw = message.channel.nsfw 
    elif isinstance(message.channel, discord.Thread):
      nsfw = message.channel.parent.nsfw
    else:
      nsfw = True

    addDataSnipe(message.author.id, message.content, current_time, nsfw)
    
    
    
  
  
  
  
  async def on_interaction(self, interaction):
    addDataU(interaction.user.id)
    if isinstance(interaction.command, discord.app_commands.Command):
      await postTips(interaction)

    
    
    



  #ON_MESSAGE
  async def on_message(self,message):
    try:
      pass
    except Exception as err:
      if hasattr(err, 'status') and err.status == 429:
        print('[ERROR] Rate-limit detected. Restarting repl')
        os.kill(1, 1)


    
    if message.author == self.user or message.author.bot:
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
      if not message.channel.permissions_for(message.guild.me).send_messages:
        return
      await message.channel.send(eval(dict(data)['autoresponse_content'])[message.content])
      return 
        
      
      
      
    if self.user.mention in message.content:
      
      if 'help' in message.content:
        em = discord.Embed(color = 0x000555,title="You need help? Get it yourself.", description = "Visit the [support server](https://discord.gg/UCGAuRXmBD)!")
        em.set_footer(text = "The embodiment of discord anarchy")
        await message.channel.send(embed = em)

      
                
        

      else:
        angry_responses = [
            "Stop pinging me.",
            "STOP PINGING ME YOU DUMB F**K",
            "Shut up, please",
            "https://imgur.com/t/mike_wazowski/lQyLC5G",
            "https://miro.medium.com/max/324/1*HI4kj-TPAQrfQkAdrw2KTA.png",
            "https://memegenerator.net/img/instances/61640131.jpg",
            
          
        ]
        await message.channel.send(random.choice(angry_responses))
          


  async def setup_hook(self):
    for filename in os.listdir('./cogs'):
      if filename.endswith('.py'):

        try:
          await bot.load_extension(f'cogs.{filename[:-3]}')
        except Exception:
          print('[ERROR] '+traceback.format_exc())
        print(f"[INFO] \033[0;32;49m{filename} loaded")
  


bot = Bot()




def backups():
  
  os.system("javac other/Backups.java")
  os.system("java other.Backups")
  


    
Thread(target=clearSnipe, name = "clearsnipe").start()
Thread(target=backups, name = "backups").start()




keep_alive()

if not os.path.exists("./logs"):
    os.makedirs("./logs")
handler = TimedRotatingFileHandler(filename='logs/discord.log', when='D', encoding='utf-8')

try:
  bot.run(os.getenv('TOKEN'), log_handler=handler)
except Exception as err:
  if hasattr(err, 'status') and err.status == 429:
    print('[ERROR] Rate-limit detected. Restarting repl')
    os.kill(1, 1)

  print('[ERROR] '+err)



    


