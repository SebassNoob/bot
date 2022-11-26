import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord import app_commands
import os
import sys
from other.asyncCmds import colorSetup,getData,getDataSnipe,getDataU,postTips, changeff
import random
import json
import base64
import aiohttp
from other.customCooldown import CustomCooldown
from other.upvoteExpiration import getUserUpvoted
import requests
from waifu import WaifuClient



import other.serverSettings as serverSettings
import asyncio
import csv
sys.path.insert(1,'./other')
from sqliteDB import create_db, get_db_connection




class Misc(commands.Cog):
  
  def __init__(self, bot):
        self.bot = bot
  



  
  @commands.command()
  @commands.check(CustomCooldown(1, 4, 1, 2, commands.BucketType.user, elements=getUserUpvoted()))
  async def pick(self,ctx,*args):
    
    
        if args ==():
          await ctx.send(f"You're missing an argument: ``list`` in that command, dumbass.")

        argList = []
        for arg in args:
          argList.append(arg)
        
        randomArg = argList[random.randint(0,len(argList)-1)]
        await ctx.send(' {}'.format(ctx.author.mention)+" I pick:\n" + randomArg)
        



  
  @commands.command(name = "predict",aliases = ["8ball"])
  @commands.check(CustomCooldown(1, 4, 1, 2, commands.BucketType.user, elements=getUserUpvoted()))
  async def predict(self,ctx,*args):
        if args ==():
          await ctx.send(f"You're missing an argument: ``question`` in that command, dumbass.")
        question = ""
        predictions = ["hmm yes i think so.","nah mate sry.","You DARE ask me this question?! Well i'm not going to give ya an answer",'not too sure about this one. try again.','Your short answer: NO',"answer's no, gtfo of here scrub.","omg YES","Are you actually stupid? Its NO.","Are you actually stupid? Its YES moron.","you gotta be kidding right, its yes.", "this question is too difficult even for my huge brain. However, at least I have one.","no.",'yes.',"you're rather stupid aren't you, answer is yes.", "You moronic bastard, its kinda obious isn't it?! NO!"]
        randomPrediction = predictions[random.randint(0,14)]
        
         

        for arg in args:
          question = question +" "+ arg

        color = int(await colorSetup(ctx.message.author.id),16)
        embedVar5 = discord.Embed(color = color)
        embedVar5.set_author(name="Question from"+' {}'.format(ctx.author), icon_url = ctx.author.avatar_url)
        embedVar5.add_field(name = question, value = randomPrediction,inline = False)
        
        embedVar5.set_footer(text="u suck")
        await ctx.channel.send(embed=embedVar5)


  autoresponse = app_commands.Group(name="autoresponse", description="The bot will respond to a list of predetermined words", guild_only=True)

  @autoresponse.command(name = "menu", description= "A list of words the bot will respond to in your server.")
  async def auto_menu(self, interaction: discord.Interaction):
    
    key_values = eval(serverSettings.get(interaction.guild_id)['autoresponse_content']).items()
    
    desc = "ID/Keyword: Response\n"
    for i, row in enumerate(key_values):
      desc=desc+f'\n{i} {row[0]}: {row[1]}'
    color = colorSetup(interaction.user.id)
    em = discord.Embed(color = color,description = f"``{desc}``")
    em.set_author(name = "Autoresponse keywords")
    em.set_footer(text="Mods can turn this off in /serversettings and edit with /autoresponse add or /autoresponse remove")
    await interaction.response.send_message(embed=em)
    

  @autoresponse.command(name="add", description="Add autoresponse keywords")
  @app_commands.checks.has_permissions(manage_guild=True)
  @app_commands.describe(word="The word you want the bot to respond to", response="The resulting response to the aforementioned word")
  async def add(self, interaction: discord.Interaction, word: str, response: str):
    to_update = serverSettings.get(interaction.guild_id)
    key_values = eval(to_update['autoresponse_content'])
    key_values.update({word: response})
    
    to_update['autoresponse_content']= f'{key_values}'
    
    serverSettings.update(interaction.guild_id, to_update)
    
    desc = "ID/Keyword: Response\n"
    for i, row in enumerate(key_values.items()):
      desc=desc+f'\n{i} {row[0]}: {row[1]}'
    color = colorSetup(interaction.user.id)
    em = discord.Embed(color = color,description = f"``{desc}``")
    em.set_author(name = "Autoresponse keywords")
    em.set_footer(text="Mods can turn this off in /serversettings and edit with /autoresponse add or /autoresponse remove")
    await interaction.response.send_message(content = f"✅ Added ``{word} : {response}``. Here is the new list.",embed=em)
    
  @autoresponse.command(name="remove", description="Remove autoresponse keywords")
  @app_commands.checks.has_permissions(manage_guild=True)
  @app_commands.describe(id="The numeric id of the word response pair you want to remove. You can check this id at  /autoresponse menu")
  async def remove(self, interaction: discord.Interaction, id: int):
    to_update = serverSettings.get(interaction.guild_id)
    key_values = list(eval(to_update['autoresponse_content']).items())
    removed = key_values.pop(id)
    #id is equal to the index of the k-v pair in items()
    res = {}
    for (k,v) in key_values:
     res[k] = v
    to_update['autoresponse_content']= f'{res}'
    serverSettings.update(interaction.guild_id, to_update)
    
    
    desc = "ID/Keyword: Response\n"
    for i, row in enumerate(key_values):
      desc=desc+f'\n{i} {row[0]}: {row[1]}'
    color = colorSetup(interaction.user.id)
    em = discord.Embed(color = color,description = f"``{desc}``")
    em.set_author(name = "Autoresponse keywords")
    em.set_footer(text="Mods can turn this off in /serversettings and edit with /autoresponse add or /autoresponse remove")
    await interaction.response.send_message(content = f"✅ Removed ``{removed[0]} : {removed[1]}``. Here is the new list.",embed=em)
    
    
  
  @commands.command()
  @commands.check(CustomCooldown(1,  14, 1, 7, commands.BucketType.user, elements=getUserUpvoted()))

  async def meme(self,ctx):
  



    subreddits = ['https://www.reddit.com/r/dankmemes/new.json?sort=hot','https://www.reddit.com/r/okbuddyretard/new.json?sort=hot','https://www.reddit.com/r/memes/new.json?sort=hot',
    'https://www.reddit.com/r/wholesomememes/new.json?sort=hot', 'https://www.reddit.com/r/meme/new.json?sort=hot', 'https://www.reddit.com/r/PrequelMemes/new.json?sort=hot','https://www.reddit.com/r/deepfriedmemes/new.json?sort=hot', 'https://www.reddit.com/r/nukedmemes/new.json?sort=hot']
    async with aiohttp.ClientSession() as cs:

      async with cs.get(subreddits[random.randint(0,len(subreddits)-1)]) as r:
        res = await r.json()
        
        color = int(await colorSetup(ctx.message.author.id),16)
        
        while True:
          try:
            randomn = random.randint(0,15)
            embed = discord.Embed(color = color,title = res['data']['children'] [randomn]["data"]["title"])
        
            embed.set_image(url=res['data']['children'] [randomn]['data']['url'])
            break

          except KeyError as e:
            raise e
            
        tip = postTips()
        
        if tip != None:
          
          await ctx.send(tip)

        await ctx.send(embed=embed)


  @commands.command()

  @commands.check(CustomCooldown(1, 6, 1, 3, commands.BucketType.user, elements=getUserUpvoted()))

  async def snipe(self,ctx, user: discord.Member):


    
    
    settings  = await getDataU()
    #implement nsfw check

    if settings[str(user.id)]["sniped"] == 0:
      await ctx.reply("This guy can't be sniped, what a loser.")
      raise Exception
    
    



    try:
      message, time, nsfw =getDataSnipe(user.id)
    #if function returns none 
    except TypeError:
      await ctx.reply("There's nothing to snipe!")
      raise Exception
    
    if ctx.channel.nsfw == False and nsfw == True:
      await ctx.send("The user you mentioned last deleted their message in a nsfw channel. 🔞")
      raise Exception
    
    color = int(await colorSetup(ctx.author.id),16)
      
    embed = discord.Embed(color= color,description=message)        
    embed.set_footer(text=f"UTC {time}")
        
    embed.set_author(name= f"{user.name}", icon_url = user.avatar_url)
    tip = postTips()
          
    if tip != None:
            
      await ctx.send(tip)
    await ctx.send(embed=embed)

  

  @commands.command()
  @commands.check(CustomCooldown(1, 6, 1, 3, commands.BucketType.user, elements=getUserUpvoted()))
  async def waifu(self,ctx):
    color = int(await colorSetup(ctx.author.id),16)
    pic = WaifuClient().sfw(category='waifu')
    em = discord.Embed(color = color)
    em.set_author(name = f"Waifu requested by {ctx.author.name}",icon_url = ctx.author.avatar_url)
    em.set_image(url = pic)
    tip = postTips()
    if tip != None:
      await ctx.send(tip)
    await ctx.send(embed = em)
    
  @commands.command()
  @commands.check(CustomCooldown(1, 6, 1, 3, commands.BucketType.user, elements=getUserUpvoted()))
  async def neko(self,ctx):
    color = int(await colorSetup(ctx.author.id),16)
    pic = WaifuClient().sfw(category='neko')
    em = discord.Embed(color = color)
    em.set_author(name = f"Neko requested by {ctx.author.name}",icon_url = ctx.author.avatar_url)
    em.set_image(url = pic)
    tip = postTips()
    if tip != None:
      await ctx.send(tip)
    await ctx.send(embed = em)
    
  @commands.command()
  @commands.check(CustomCooldown(1, 6, 1, 3, commands.BucketType.user, elements=getUserUpvoted()))
  async def shinobu(self,ctx):
    color = int(await colorSetup(ctx.author.id),16)
    pic = WaifuClient().sfw(category='shinobu')
    em = discord.Embed(color = color)
    em.set_author(name = f"Neko requested by {ctx.author.name}",icon_url = ctx.author.avatar_url)
    em.set_image(url = pic)
    tip = postTips()
    if tip != None:
      await ctx.send(tip)
    await ctx.send(embed = em)
    
  @commands.command()
  @commands.check(CustomCooldown(1, 86400, 1, 86400, commands.BucketType.user, elements=getUserUpvoted()))
  async def daily(self,ctx):
    color = int(await colorSetup(ctx.author.id),16)
    em = discord.Embed(color = color,description = "You've claimed your daily and recieved 30 minutes of lower cooldowns. [Upvote](https://top.gg/bot/844757192313536522) me to get a 12h extension!")
    await ctx.send(embed = em)
    with open("./json/upvoteData.json","r") as f:
      file= json.load(f)
  
    try:
      d = {str(ctx.author.id): file[str(ctx.author.id)]+30}

      file.update(d)
    except KeyError:
      file[str(ctx.author.id)] = 30
    
    
    with open("./json/upvoteData.json","w") as f:
      json.dump(file,f)
      f.close


  @commands.command()
  async def iplookup(self,ctx,ip: str):
    color = int(await colorSetup(ctx.author.id),16)
    url = f"http://ip-api.com/json/{ip}"
    res = requests.get(url).json()
    
    for item in res.items():
      if item[0] == "status":
        if item[1] =="success":
          
          pass
        else:
          
          await ctx.send("Thats not a valid ip, idiot.")
          
          
    try:
      country = res["country"] or "Unknown" 
      region = res["regionName"] or "Unknown" 
      city = res["city"] or "Unknown"  
      zip= res["zip"] or "Unknown" 
      latitude = res['lat'] or "Unknown"  
      longitude = res['lon'] or "Unknown" 
      provider = res['isp'] or "Unknown" 
    except:
      await ctx.send("An unspecified error occured, the ip address probably is private. What a loser lmao.")
    await ctx.send(embed =discord.Embed(color = color, title = ip,description = f"**country**:{country}\n**region**:{region}\n**city**:{city}\n**zip code**:{zip}\n**coordinates**: ({latitude},{longitude})\n**ISP**:{provider}"))
      

  @commands.command()
  @commands.check(CustomCooldown(1, 10, 1, 5, commands.BucketType.user, elements=getUserUpvoted()))
  async def textwall(self,ctx,num:int,*content):
    #print(len(content))
    #print(content)
    if len(content) == 0:
      await ctx.send("You forgot to say what you want to textwall! You're such an idiot.")
      raise Exception("no args passed into textwall")
    sents=""
    for word in content:
      sents = sents+ f" {word}"

    sents = sents[1:]
    toSend= ""
    for i in range(num):
      toSend = toSend + f" {sents}"

    if len(toSend) > 2000:
      await ctx.send("Your text wall is too long (>2000 characters), you moron. ")
      raise Exception("textwall too long")
    if await familyFriendlySetup(ctx.author.id):
      toSend = await changeff(toSend)
    await ctx.send(toSend)

  @commands.command()
  async def urbandict(self,ctx,term):
    
  
    url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
    
    querystring = {"term":term}
    
    headers = {
        'x-rapidapi-key': "eb9abc1708msh9ff61d9af0e2802p1a89dejsncd366a92c2b6",
        'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com"
        }
    
    response = requests.request("GET", url, headers=headers, params=querystring)
    color = int(await colorSetup(ctx.message.author.id),16)
    try:
      em = discord.Embed(color = color, title=f"Urban Dictionary result for {term}", description = "Definition: "+response.json()['list'][0]["definition"]+"\n\nExamples: "+response.json()['list'][0]["example"])
      await ctx.send(embed = em)
    except:
      await ctx.send("there were no results returned, actually search for a real word next time, you moron.")
    
  
async def setup(bot):
  await bot.add_cog(Misc(bot))

