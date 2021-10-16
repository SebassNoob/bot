import os
import random
import discord
from other.asyncCmds import addData,colorSetup,getData,addDataSnipe,getDataSnipe
import math
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
from keep_alive import keep_alive
import datetime
import asyncio
import json
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType,Select,SelectOption
from other.upvoteExpiration import upvoteCheck
from threading import Thread
from other.asyncCmds import egg,postTips
import time
from other.snipeTimeout import snipeTimeout, encodeCache
import sys
import csv
intents = discord.Intents.default()


def get_prefix(bot, message): 
  try:
    with open('./json/serverData.json', 'r') as f: 
      prefixes = json.load(f) 
    return prefixes[str(message.guild.id)]['Prefix']
  except KeyError:
    return '$'

    
bot = commands.AutoShardedBot(command_prefix=get_prefix, help_command = None, intents=intents,shard_count=4)

DiscordComponents(bot)


@bot.event
async def on_ready():
  
  servers = len(bot.guilds)
  

  print("\033[0;36;48m-----------------------------------------")
  print(" * "+'{0.user}'.format(bot)+ f" connected to {servers} servers")
  
  servers = len(bot.guilds)
  count = {}
  for guild in bot.guilds:
    if guild.shard_id not in count:
      count[guild.shard_id] = 1
    else:
      count[guild.shard_id] += 1
  for t in count.items():
    
    print(f"   - Shard {t[0]}: {t[1]} servers")
  print("\033[0;36;48m-----------------------------------------")
  await bot.change_presence(activity=discord.Game(name="$help"))
  
  



@bot.event
async def on_command_error(ctx, error):
  
  
  if isinstance(error, discord.ext.commands.errors.CommandNotFound):
    
    raise Exception("CommandNotFound")
    
  if isinstance(error, discord.ext.commands.MissingRequiredArgument):
        em = discord.Embed(color = 0x000000, description = f"You're missing an argument: ``{error.param}`` in that command, dumbass.")
        await ctx.reply(embed = em)
        raise Exception("MissingRequiredArgument")
        
  if isinstance(error,commands.CommandInvokeError):
    
    if str(error) == "Command raised an exception: NotFound: 404 Not Found (error code: 10008): Unknown Message":
      raise Exception("NotFound")
    if str(error) == "Command raised an exception: ClientException: Already connected to a voice channel.":
      await ctx.send(embed = discord.Embed(color = 0x000000, description = "The bot is already connected to a voice channel, dumbass."))
    if str(error).startswith("Command raised an exception: Exception:"):
      pass
    else:
      em = discord.Embed(color = 0x000000,title = "Unknown error.", description = f"Please report this to the [support server](https://discord.gg/UCGAuRXmBD).\nFull traceback:\n```py\n{error}```")
      await ctx.send(embed = em)
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
      
    
  


@bot.event
async def on_guild_join(guild):
  print(guild.name)
  await addData(guild.id)
  for channel in guild.text_channels:
    if channel.permissions_for(guild.me).send_messages:
      
      em = discord.Embed(color = 0x000555,title="A very suitable welcome message", description = "Hey, annoybot here. My prefix is $, and if you need any help, visit the [support server](https://discord.gg/UCGAuRXmBD)!")
      em.set_footer(text = "The embodiment of discord anarchy")
      await channel.send(embed = em)
      break









#commands below
@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  else:
    await bot.process_commands(message)
    
  try:
    
    
    await addData(message.guild.id)
    guildId = message.guild.id
    guilds = await getData()
    if guilds[str(guildId)]["autoresponse"] == 1:
      
      arr = []
      with open("./json/autoresponse.csv",newline="") as file:
        reader = csv.DictReader(file)
        
        for row in reader:
          arr.append(row)
        
        for keyword in arr:
          
          if keyword["word"] in message.content.split(" "): 
            await message.channel.send(keyword["response"].replace(";",","))
  
    if f'<@{bot.user.id}>' in message.content or f'<@!{bot.user.id}>' in message.content :
      
      if 'help' in message.content:
        em = discord.Embed(color = 0x000555,title="You need help? Get it yourself.", description = " My prefix is $, and if you need any help, visit the [support server](https://discord.gg/UCGAuRXmBD)!")
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
          
          
          
          
        
  except Exception:
    pass
  
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
      
    
  
    





@bot.event
async def on_message_delete(message):

  
  await addDataSnipe(message.author.id)
  users = await getDataSnipe()
  
  current_time = datetime.datetime.now() 
  
  if len(str(current_time.minute)) ==1:
    minute = "0"+str(current_time.minute)

  else:
    minute = str(current_time.minute)


  cur_time = str(current_time.day) +'-'+str(current_time.month) +'-'+str(current_time.year) +' at ' +str(current_time.hour) +':' + minute

  
  d = {"deletedMessage" : str(message.content), "date" : cur_time}
  users[str(message.author.id)].update(d)
  
  if message.channel.nsfw ==False:
    e = {"nsfw": False,"encoded":False}
    users[str(message.author.id)].update(e)
  elif message.channel.nsfw ==True:
    e = {"nsfw": True,"encoded":False}
    users[str(message.author.id)].update(e)
    
  
  
  with open("./json/userSnipeCache.json","w") as f:
    json.dump(users,f)


    

@bot.command()
async def patchnotes(ctx):
  color = int(await colorSetup(ctx.message.author.id),16)
  em = discord.Embed(color = color)
  em.add_field(name = "1.7.1", value = "-New commands: suggest\n-Rework: autoresponse\n-typo fix",inline = False)
  await ctx.send(embed = em)





#cogs
for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')
    print(f"\033[0;32;49m{filename} loaded")
    

import topgg




bot.topggpy = topgg.DBLClient(bot, os.getenv('topgg token'), autopost=True, post_shard_count=True)


@bot.event
async def on_autopost_success():
    print(
        f"Posted server count ({bot.topggpy.guild_count}), shard count ({bot.shard_count})"
    )

@bot.command()
async def servers(ctx):
  for server in bot.guilds:
    print(server.name, server.id)

@bot.command()
async def sysexit(ctx):
  
  if int(ctx.author.id) == int(os.getenv("uid")):
    await ctx.send("Bot has been taken offline.")
    sys.exit()



Thread(target=upvoteCheck).start()
Thread(target=snipeTimeout).start()
Thread(target=encodeCache).start()

keep_alive() 

bot.run(os.getenv('TOKEN'))

