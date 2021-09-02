import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

from other.asyncCmds import colorSetup,addData,getData,addDataSnipe,getDataSnipe,getDataU,postTips
import random
import json
import base64
import aiohttp
from other.customCooldown import CustomCooldown
from other.upvoteExpiration import getUserUpvoted
import requests
from waifu import WaifuClient
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
  @has_permissions(manage_messages=True)  
  async def autoresponse(self,ctx,arg=None):
    guildId = ctx.message.guild.id
    
    await addData(guildId)
    
    guilds = await getData()
    status =["Disabled :x: ","Enabled :white_check_mark: "]
    
    
    if arg == "Nword" or arg == "nword":
    
      await addData(guildId)
      guilds = await getData()
      if guilds[str(guildId)]["Nword"] == 0:
        d1 = {"Nword": 1}
      elif guilds[str(guildId)]["Nword"] ==1:
        d1 = {"Nword": 0}
      
      guilds[str(guildId)].update(d1)
      with open("./json/serverData.json","w") as f:
        json.dump(guilds,f)
      await ctx.send("N-word is now **"+status[guilds[str(guildId)]["Nword"]]+"**")
      #change state

    elif arg == "Fword" or arg == "fword":
    
      await addData(guildId)
      guilds = await getData()
      if guilds[str(guildId)]["Fword"] == 0:
        d1 = {"Fword": 1}
      elif guilds[str(guildId)]["Fword"] ==1:
        d1 = {"Fword": 0}
      
      guilds[str(guildId)].update(d1)
      with open("./json/serverData.json","w") as f:
        json.dump(guilds,f)
      await ctx.send("F-word is now **"+status[guilds[str(guildId)]["Fword"]]+"**")
      #change state

    elif arg == "Cword" or arg == "cword":
    
      await addData(guildId)
      guilds = await getData()
      if guilds[str(guildId)]["Cword"] == 0:
        d1 = {"Cword": 1}
      elif guilds[str(guildId)]["Cword"] ==1:
        d1 = {"Cword": 0}
      
      guilds[str(guildId)].update(d1)
      with open("./json/serverData.json","w") as f:
        json.dump(guilds,f)
      await ctx.send("C-word is now **"+status[guilds[str(guildId)]["Cword"]]+"**")
      #change state
    
    if arg == None:
      NwordValue = guilds[str(guildId)]["Nword"]
      FwordValue = guilds[str(guildId)]["Fword"]
      CwordValue = guilds[str(guildId)]["Cword"]
    
      color = int(await colorSetup(ctx.message.author.id),16)
      em = discord.Embed(color = color)
      em.set_author(name = "Autoresponse settings")
      em.add_field(name = "N-word",value = status[int(NwordValue)],inline= False)
      em.add_field(name = "F-word",value = status[int(FwordValue)],inline= False)
      em.add_field(name = "C-word",value = status[int(CwordValue)],inline= False)
      await ctx.send(embed=em)
      #print state

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


    uid = ctx.author.id
    await addDataSnipe(user.id)
    await addDataSnipe(uid)
    users = await getDataSnipe()
    
    settings  = await getDataU()
    async def command():
      color = int(await colorSetup(ctx.author.id),16)
      if users[str(user.id)]["encoded"] == True:
        message = str(base64.b64decode(users[str(user.id)]["deletedMessage"]))[2:-1]
        
      else:
        
        message = users[str(user.id)]["deletedMessage"]
      embed = discord.Embed(color= color,description=message)        
      embed.set_footer(text="UTC "+users[str(user.id)]["date"])
        
      embed.set_author(name= f"{user.name}", icon_url = user.avatar_url)
      tip = postTips()
          
      if tip != None:
            
        await ctx.send(tip)
      await ctx.send(embed=embed)
          
    try:
      if users[str(user.id)]["deletedMessage"]=='':
        await ctx.reply("There's nothing to snipe!")
        raise Exception
      if settings[str(user.id)]["sniped"] == 0:
        await ctx.reply("This guy can't be sniped, what a loser.")
      else:
        if ctx.channel.nsfw == False and users[str(user.id)]["nsfw"] == False:   
          await command()
        elif ctx.channel.nsfw == True and users[str(user.id)]["nsfw"] == False:   
          await command()
        elif ctx.channel.nsfw == False and users[str(user.id)]["nsfw"] == True:   
          await ctx.send("The user you mentioned deleted their last message in an nsfw channel.😳")
        elif ctx.channel.nsfw == True and users[str(user.id)]["nsfw"] == True:   
          await command()
    except:
      pass
  
  

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
def setup(bot):
    bot.add_cog(Misc(bot))