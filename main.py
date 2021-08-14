import os
import numexpr
import discord
from other.asyncCmds import addData,colorSetup,getData,addDataSnipe,getDataSnipe
import math
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
from keep_alive import keep_alive
import datetime
import asyncio
import json
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
from other.upvoteExpiration import upvoteCheck
from threading import Thread
from other.asyncCmds import egg
import time
intents = discord.Intents.default()
intents.members = True

def get_prefix(bot, message): 
  try:
    with open('./json/serverData.json', 'r') as f: 
      prefixes = json.load(f) 
    return prefixes[str(message.guild.id)]['Prefix']
  except KeyError:
    return '$'

    
bot = commands.Bot(command_prefix=get_prefix, help_command = None, intents=intents)


DiscordComponents(bot)

@bot.event
async def on_ready():
  servers = len(bot.guilds)
  
  print("\033[0;36;48m-------------------------------------")
  print('\033[0;36;48m{0.user}'.format(bot)+ " connected to " + str(servers) + " servers")
  print("\033[0;36;48m-------------------------------------")
  
  




@bot.event
async def on_command_error(ctx, error):
    
    if isinstance(error, discord.ext.commands.MissingRequiredArgument):
        await ctx.reply("You're missing an argument in that command, dumbass.")
        pass
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.reply('This command is on a **%.1fs** cooldown, not sorry.' % error.retry_after)
        pass
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply(":redTick: You don't have permission to use that command.")
        pass
    if isinstance(error, discord.ext.commands.CommandNotFound):
        
        pass
    
    else:
      raise error




@bot.event
async def on_guild_join(guild):
  await addData(guild.id)









#commands below
@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  else:
    await bot.process_commands(message)
    
  try:
    

    guildId = message.guild.id
    guilds = await getData()
    NwordValue = guilds[str(guildId)]["Nword"]
    FwordValue = guilds[str(guildId)]["Fword"]
    CwordValue = guilds[str(guildId)]["Cword"]
    if NwordValue == 1:
      if "nigga" in message.content or "nigger" in message.content or "Nigga" in message.content or "Nigger" in message.content:
        await message.channel.send("You have been captured saying the Nword in 4K! STFU U RASIST SCUM.")

    if FwordValue == 1:
      if "fuck" in message.content or "Fuck" in message.content:
        await message.channel.send("Frick off, you've been seen dropping an f bomb. ")
        
    if CwordValue == 1:
      if "cunt" in message.content or "Cunt" in message.content:
        await message.channel.send("You've been caught saying the worst word in the english language. Reevaluate your life choices.")

  
    if f'<@{bot.user.id}>' in message.content or f'<@!{bot.user.id}>' in message.content :
      
      if 'help' in message.content:
        await message.channel.send("Hey, use $cmds to show my list of commands!")
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
            for i in range(10):
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
  
    file[data] = 720
    
    with open("./json/upvoteData.json","w") as f:
      json.dump(file,f)
      f.close
      
    
    user = bot.get_user(int(data))
    
    
    await user.send("Thanks for upvoting! You received lower cooldowns for all commands.")
    
















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
  

  with open("./json/userSnipeCache.json","w") as f:
    json.dump(users,f)
  
    

@bot.command()
async def patchnotes(ctx):
  color = int(await colorSetup(ctx.message.author.id),16)
  em = discord.Embed(color = color)
  em.add_field(name = "1.6.1 patch", value = "-New commands: shinobu, wouldyourather(wyr)\n-Fixed tictactoe and memorygame to not return errors while playing simultaneously\n-More tips\n-fixed ``$meme`` not responding (hopefully)\n-simplified ``$settings`` to be consistant with the rest of the setup commands",inline = False)
  await ctx.send(embed = em)







#cogs
for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')



Thread(target=upvoteCheck).start()



keep_alive() 


bot.run(os.getenv('TOKEN'))
