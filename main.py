import os
import numexpr
import discord
from other.asyncCmds import addData,colorSetup,getData,addDataSnipe,getDataSnipe
import math
from discord.ext import commands
from discord.ext.commands import has_permissions
from keep_alive import keep_alive
import datetime
import asyncio
import json
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType




def get_prefix(bot, message): 
  try:
    with open('./json/serverData.json', 'r') as f: 
      prefixes = json.load(f) 
    return prefixes[str(message.guild.id)]['Prefix']
  except KeyError:
    return '$'

    
bot = commands.Bot(command_prefix=get_prefix, help_command = None)


DiscordComponents(bot)

@bot.event
async def on_ready():
  servers = len(bot.guilds)
  print("-------------------------------------")
  print('{0.user}'.format(bot)+ " connected to " + str(servers) + " servers")
  print("-------------------------------------")
  
  




@bot.event
async def on_command_error(ctx, error):
    
    if isinstance(error, discord.ext.commands.MissingRequiredArgument):
        await ctx.reply("You're missing an argument in that command, dumbass.")
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.reply('This command is on a **%.1fs** cooldown, not sorry.' % error.retry_after)
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply(":redTick: You don't have permission to use that command.")
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


    if f'<@!{bot.user.id}>' in message.content and 'help' in message.content:
      await message.channel.send("Hey, use $cmds to show my list of commands!")
  except Exception:
    pass
















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
  em.add_field(name = "1.4.0 patch", value = "-Removed spam command since it's considered api abuse.\n-New command- fakeban\n-New command - dmthreaten\n-Updated all main features with new command possibilities\n-Form has 2 new subcommands\n-typos fixed\n-Most troll commands nerfed to prevent api abuse.\nHotfix 25/7 -fixed fakemute not working",inline = False)
  await ctx.send(embed = em)







#cogs
for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')

keep_alive()       
bot.run(os.getenv('TOKEN'))