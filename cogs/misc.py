import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

import os
import sys
from other.asyncCmds import colorSetup,getData,addDataSnipe,getDataSnipe,getDataU,postTips
import random
import json
import base64
import aiohttp
from other.customCooldown import CustomCooldown
from other.upvoteExpiration import getUserUpvoted
import requests
from waifu import WaifuClient
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType,Select,SelectOption
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
        

  @commands.command(name = "autoresponse")

  @commands.check(CustomCooldown(1, 4, 1, 2, commands.BucketType.user, elements=getUserUpvoted()))
 
  async def autoresponse(self,ctx):
    arr=[]
    guildId = ctx.message.guild.id
    
    try:
      #tries to create db with guildId as name, under ./other/data
      #uses schema.sql as format
      #if already exists error raised, ignore new creation
      create_db(f'./other/data/{guildId}.db','./other/schema.sql')
      print(f"created {guildId}")
    except:
      pass
    conn = get_db_connection(f'./other/data/{guildId}.db')
    cur = conn.cursor()
    data = conn.execute('SELECT * FROM autoresponse ORDER BY id').fetchall()
    
    if len(data)== 0:
      
      with open("./json/autoresponse.csv",newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            arr.append(row)
        for pair in arr:
          conn.execute('INSERT INTO autoresponse (keyword,res) VALUES (?,?)',(pair["word"],pair["response"]))
          conn.commit()



    desc = "ID/Keyword: Response\n"
    for row in cur.execute('SELECT * FROM autoresponse'):
      desc=desc+f'\n{row[0]} {row[1]}: {row[2]}'

    
    guilds = await getData()

    
    
    
    color = int(await colorSetup(ctx.message.author.id),16)
    em = discord.Embed(color = color,description = f"``{desc}``")
    em.set_author(name = "Autoresponse keywords")
    button_color = "" #for on/off
    label = "" #for on/off
    
    
    disabled_button = None
    if guilds[str(guildId)]["autoresponse"] == 1:
      button_color= ButtonStyle.green
      label = "on"
      
    elif guilds[str(guildId)]["autoresponse"] == 0:
      button_color = ButtonStyle.red
      label = "off"
      
    if ctx.author.guild_permissions.manage_messages == True or int(ctx.author.id) == int(os.getenv("uid")):
      disabled_button = False
    elif ctx.author.guild_permissions.manage_messages == False:
      disabled_button = True
    msg = await ctx.send(embed=em, 
    components = [ 
              [
                  Button(
                      label = label,
                      id = "selector",
                      style = button_color,
                      disabled = disabled_button
                      
                  ),
                  Button(
                    label = "Add",
                    id="add",
                    style= ButtonStyle.blue,
                    disabled = disabled_button
                    
                  ),
                  Button(
                    label = "Remove",
                    id="rm",
                    style= ButtonStyle.blue,
                    disabled = disabled_button
                    
                  )
              ]])
    
    
    
    while True:
      try:
        interaction = await self.bot.wait_for(
                  "button_click",
                  check = lambda i: i.component.id in ["selector","add","rm"] and i.channel.id == ctx.channel.id, 
                  timeout = 30.0 
              )
              
        if interaction.user.id != ctx.author.id:
          await interaction.respond(type=4, content="This isn't your menu, idiot.", ephemeral=True)
          
        def write():
          
          with open("./json/serverData.json","w") as f:
            
            json.dump(guilds,f)
            f.close()

        if interaction.component.id == "selector":
          if guilds[str(guildId)]["autoresponse"] == 1:        
            d = {"autoresponse" : 0}
            guilds[str(ctx.guild.id)].update(d)
            button_color= ButtonStyle.red
            label = "off"
            write()
          
      
          elif guilds[str(guildId)]["autoresponse"] == 0:
            d = {"autoresponse" : 1}
            guilds[str(ctx.guild.id)].update(d)
            button_color= ButtonStyle.green
            label = "on"
            write()   

        if interaction.component.id == "add":
            
            await interaction.respond(type=4,content="what keyword would you like to add?",ephemeral=False)
            
            key= await self.bot.wait_for("message",check = lambda i: i.channel.id==ctx.channel.id and i.author.id == ctx.author.id, timeout=None)
            await ctx.send("what should the response be?")


            res= await self.bot.wait_for("message",check = lambda i: i.channel.id==ctx.channel.id and i.author.id == ctx.author.id, timeout=None)
            conn.execute('INSERT INTO autoresponse (keyword,res) VALUES (?,?)',(key.content,res.content))
            await ctx.send("confirmed")
            disabled_button= True

        if interaction.component.id == "rm":
            
            await interaction.respond(type=4,content="type the id of the autoresponse pair you want to delete.",ephemeral=False)
            
            id= await self.bot.wait_for("message",check = lambda i: i.channel.id==ctx.channel.id and i.author.id == ctx.author.id, timeout=None)
            try:
              id = int(id.content)
              cur.execute('DELETE FROM autoresponse WHERE id=(?)',(id,))
              await ctx.send("confirmed.")
              disabled_button = True
            except:
              await ctx.send("don't be an idiot you donkey, actually provide an id number.")
              disabled_button=True
        
        conn.commit()
        desc = "ID/Keyword: Response\n"
        for row in cur.execute('SELECT * FROM autoresponse'):
          desc=desc+f'\n{row[0]} {row[1]}: {row[2]}'

    
    

    
    
    
        color = int(await colorSetup(ctx.message.author.id),16)
        em = discord.Embed(color = color,description = f"``{desc}``")
        await msg.edit(embed=em)
        await interaction.respond(                     
                      type = InteractionType.UpdateMessage,
                      
                      components = [[
      
                  Button(
                      label = label,
                      id = "selector",
                      style = button_color,
                      disabled = disabled_button
                      
                  ),
                  Button(
                    label = "Add",
                    id="add",
                    style= ButtonStyle.blue,
                    disabled = disabled_button
                    
                  ),
                  Button(
                    label = "Remove",
                    id="rm",
                    style= ButtonStyle.blue,
                    disabled = disabled_button
                    
                  )
              ]])
      except asyncio.TimeoutError:
        await msg.delete()
        
  

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
  @commands.check(CustomCooldown(1, 0, 1, 0, commands.BucketType.user, elements=getUserUpvoted()))
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
      
    await ctx.send(toSend)
  
def setup(bot):
    bot.add_cog(Misc(bot))

