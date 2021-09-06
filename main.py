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

intents = discord.Intents.default()



def get_prefix(bot, message): 
  try:
    with open('./json/serverData.json', 'r') as f: 
      prefixes = json.load(f) 
    return prefixes[str(message.guild.id)]['Prefix']
  except KeyError:
    return '$'

    
bot = commands.AutoShardedBot(command_prefix=get_prefix, help_command = None, intents=intents,shard_count=3)

DiscordComponents(bot)


@bot.event
async def on_ready():
  
  servers = len(bot.guilds)
  count = {}
  for guild in bot.guilds:
    if guild.shard_id not in count:
      count[guild.shard_id] = 1
    else:
      count[guild.shard_id] += 1
  print(count)

  
  print("\033[0;36;48m-------------------------------------")
  print('\033[0;36;48m{0.user}'.format(bot)+ " connected to " + str(servers) + " servers")
  print("\033[0;36;48m-------------------------------------")
  await bot.change_presence(activity=discord.Game(name="$help"))
  
  
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



@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, discord.ext.commands.errors.CommandNotFound):
    
    raise Exception("CommandNotFound")
    
  if isinstance(error, discord.ext.commands.MissingRequiredArgument):
        em = discord.Embed(color = 0x000000, description = f"You're missing an argument: ``{error.param}`` in that command, dumbass.")
        await ctx.reply(embed = em)
        raise Exception("MissingRequiredArgument")
        
  if isinstance(error,commands.CommandInvokeError):
    raise Exception("CommandInvokeError")
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
        em = discord.Embed(color = 0x000000, description = f":redTick: You need the {error.missing_perms} permission to use that command.")
        await ctx.reply(embed = em)
        raise Exception("MissingPermissions")
    
  if isinstance(error, discord.ext.commands.errors.BotMissingPermissions):
        em = discord.Embed(color = 0x000000, description = f"I don't have permissions for that! I need the {error.missing_perms} permission(s).")
        await ctx.send(embed = em)
        raise Exception("BotMissingPermissions")
  if isinstance(error, discord.ext.commands.errors.MemberNotFound):
        em = discord.Embed(color = 0x000000, description = "The member you mentioned was not found, actually send a member name next time you moron.")
        await ctx.send(embed = em)
        raise Exception("MemberNotFound")
      
    
  else:
    
    
      em = discord.Embed(color = 0x000000,title = "Unknown error.", description = f"Please report this to the [support server](https://discord.gg/UCGAuRXmBD).\nFull traceback:\n```py\n{error}```")
      await ctx.send(embed = em)
      raise error














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
        color = int(await colorSetup(message.author.id),16)
        embedVar = discord.Embed(color = color)
        embedVar.set_author(name="Annoybot commands")
        embedVar.add_field(name = "``roast (*user)``", value = "Give[s](<https://www.bit.ly/IqT6zt>) a random roast to a mentioned user. (40 possibilities)\n**6**s cooldown.",inline = False)
        
        embedVar.add_field(name = "``swear``", value = "The bot will swear at you.\n**6**s cooldown.",inline = False)
        embedVar.add_field(name = "``urmom``", value = "Gives a random Ur Momma joke. (30 possibilities)\n**6**s cooldown.",inline = False)
        embedVar.add_field(name = "``uninspire``", value = "Gives a random uninspirational quote. (20 possibilities)\n**6**s cooldown.",inline = False)
        embedVar.add_field(name = "``dmthreaten (user,*reason)``", value = "The bot DMs a user and threaten them. (10 possibilities)\n**10**s cooldown.",inline = False)
        embedVar.add_field(name = "``dadjoke``", value = "Sends a dad joke.\n**10**s cooldown.",inline = False)
          
        

        
        embedVar2 = discord.Embed(color = color)
        embedVar2.set_author(name="Annoybot commands (math)\n All commands have a 10s cooldown.")
            
        embedVar2.add_field(name = "``calc (expression)``", value = "Evaluates your expression. Functions include:\n `+`,`-`,`*`,`/`,`sqrt`,`log`,`sin`,`cos`,`tan`.",inline = False)
            
        embedVar2.add_field(name = "``form circleArea (x)``", value = "Returns the area of a circle with radius x.",inline = True)
        embedVar2.add_field(name = "``form circleCircum (x)``", value = "Returns the circumference of a circle with radius x.",inline = True)
        embedVar2.add_field(name = "``form triangleArea (x,y)``", value = "Returns the area of a triangle with base x and height y.",inline = True)
        embedVar2.add_field(name = "``form pythagoras (x,y)``", value = "Returns the length of hypotenuse of triangle base x and height y.",inline = True)
        embedVar2.add_field(name = "``form sphereVol (x)``", value = "Returns volume of sphere with radius x.",inline = True)
        embedVar2.add_field(name = "``form sphereArea (x)``", value = "Returns surface area of sphere with radius x.",inline = True)
        
        

        embedVar3 = discord.Embed(color = color)
        embedVar3.set_author(name="Annoybot commands (misc)")
        embedVar3.add_field(name = "``pick (list)``", value = "Randomly chooses from a list of arguments the user provides.\n**4**s cooldown.",inline = False)
        embedVar3.add_field(name = "``predict (question)``", value = "Predicts the answer to a yes/no question.\n**4**s cooldown.",inline = False)
        embedVar3.add_field(name = "``autoresponse``", value = "Responds to certain keywords guild-wide and sends a message in return. \nRequires user to have **manage_messages** permission.\n**4**s cooldown.",inline = False)
        embedVar3.add_field(name = "``meme``", value = "Sends a meme.\n**14**s cooldown.",inline = False)
        embedVar3.add_field(name = "``snipe (user)``", value = "Shows a user's recently deleted message.\n**6**s cooldown",inline = False)
        embedVar3.add_field(name = "``waifu``", value = "Shows a picture of a waifu.\n**6**s cooldown",inline = False)
        embedVar3.add_field(name = "``neko``", value = "Shows a picture of a neko.\n**6**s cooldown",inline = False)
        embedVar3.add_field(name = "``shinobu``", value = "Shows a picture of a shinobu.\n**6**s cooldown",inline = False)
        
        
        

        embedVar4 = discord.Embed(color = color)
        embedVar4.set_author(name="Annoybot commands (trolls)\n All troll commands have a 10s cooldown.")
        
        embedVar4.add_field(name = "``channeltroll (user)``", value = "Creates a private new channel and pings the trolled user 3 times. When either the trolled user speaks in the channel or 2 minutes have passed, the channel is deleted.\nRequires bot to have **manage_channels** permission.",inline = False)
        embedVar4.add_field(name = "``nicktroll (user)``", value = "Changes the nickname of a user temporarily to either a random set of characters or a chosen nickname.\nRequires bot to have **manage_nicknames** permission.",inline = False)
        embedVar4.add_field(name = "``dmtroll (user)``", value = "Ping the affected user 3 times in their dms, then deletes it.",inline = False)

        embedVar4.add_field(name = "``ghosttroll (user)``", value = "Ghost pings the user in 3 different channels.",inline = False)
        

        embedVar4.add_field(name = "``fakeban (user)``", value = "Fakes a ban for the trolled user. WARNING: USER WILL BE KICKED. Requires bot to have **create_instant_invite** and **kick_members** permissions and user needs **kick_members** permission. ",inline = False)

        embedVar4.add_field(name = "``fakemute (user,*reason)``", value = "Fakes a mute for the trolled user. If no reason is given, a random one will be generated. ",inline = False)


        embedVar5 = discord.Embed(color = color)
        embedVar5.set_author(name="Annoybot commands (games)\nAll games commands have a 10s cooldown.")
        embedVar5.add_field(name = "``memorygame``", value = "Memorise the pattern shown at the start of the level and try to replicate it from memory afterward.",inline = False)
        embedVar5.add_field(name = "``tictactoe (user)``", value = "Play tictactoe with a friend!",inline = False)
        embedVar5.add_field(name = "``vocabularygame``",value = "Test your vocabulary skills with this game! Requires bot to have **add_reaction** permission.", inline = False)
        embedVar5.add_field(name = "``typingrace``",value = "Race with others and see who can type the fastest!", inline = False)
        embedVar5.add_field(name = "``wouldyourather``",value = "Challenge your friends to a would you rather game. Best experienced in a VC!", inline = False)
        embedVar5.add_field(name = "``truthordare``", value = "Play a game of truth or dare with your friends. Best played in a VC or physically!", inline = False)
        
        embedVar6 = discord.Embed(color = color)
        embedVar6.set_author(name="Annoybot commands (setup)")
        embedVar6.add_field(name = "``daily``", value = "Gives you 30mins of reduced cooldowns once per day!",inline = False)
        embedVar6.add_field(name = "``patchnotes``", value = "Shows the latest patch notes!",inline = False)
        embedVar6.add_field(name = "``settings (*option, *value)``", value = "Shows user settings. ",inline = False)
        embedVar6.add_field(name = "``changeprefix (prefix)``", value = "Changes the bot's prefix in the server.",inline = False)
        embedVar6.add_field(name = "``vote``", value = "Sends links to support this bot!",inline = False)
        embedVar6.add_field(name = "``resetdata``", value = "Resets and removes all your data from the bot.", inline = False)

        paginationList = [embedVar,embedVar2,embedVar3,embedVar4,embedVar5,embedVar6]
        
        current = 0
        tip = postTips()
            
        if tip != None:
          await message.channel.send(tip)
        instruct = await message.channel.send("The values in brackets are additional arguments you're supposed to give. * denotes an optional argument.")
        mainMessage = await message.channel.send(
            
            embed = paginationList[current],
            components = [ 
              Select(placeholder="Other pages", options=[SelectOption(label="Main features", value="0"), SelectOption(label="Math", value="1"), SelectOption(label="Misc", value="2"), SelectOption(label="Trolls", value="3"), SelectOption(label="Games", value="4"), SelectOption(label="Setup", value="5")])
            ]
        )
        
        while True:
            
            try:
                interaction = await bot.wait_for(
                    "select_option", 
                    check = lambda i: i.component[0].value in["0","1","2","3","4","5"],
                    timeout = 30.0 
                )
                
                

                current = int(interaction.component[0].value)
                await interaction.respond(
                    type = InteractionType.UpdateMessage,
                    embed = paginationList[current],
                  
                )
            except asyncio.TimeoutError:
              await mainMessage.delete()
              await instruct.delete()
                
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
  em.add_field(name = "1.6.3", value = "-New command: truthordare, daily\n-Bugfixes for games\n-UI improvements for errors\n-More tips\n-Another easter egg",inline = False)
  await ctx.send(embed = em)





#cogs
for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')



Thread(target=upvoteCheck).start()
Thread(target=snipeTimeout).start()
Thread(target=encodeCache).start()

keep_alive() 


bot.run(os.getenv('TOKEN'))
