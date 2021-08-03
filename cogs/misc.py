import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

from other.asyncCmds import colorSetup,addData,getData,addDataSnipe,getDataSnipe,getDataU,postTips
import random
import json

import aiohttp
from other.customCooldown import CustomCooldown
from other.upvoteExpiration import getUserUpvoted

class Misc(commands.Cog):
  
  def __init__(self, bot):
        self.bot = bot
  


  
  @commands.command()
  @commands.check(CustomCooldown(1, 4, 1, 2, commands.BucketType.user, elements=getUserUpvoted()))
  async def pick(self,ctx,*args):
    
        argList = []
        for arg in args:
          argList.append(arg)
        
        randomArg = argList[random.randint(0,len(argList)-1)]
        await ctx.send(' {}'.format(ctx.author.mention)+" I pick:\n" + randomArg)
        


  
  @commands.command(name = "predict",aliases = ["8ball"])
  @commands.check(CustomCooldown(1, 4, 1, 2, commands.BucketType.user, elements=getUserUpvoted()))
  async def predict(self,ctx,*args):
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
  @commands.check(CustomCooldown(1, 14, 1, 7, commands.BucketType.user, elements=getUserUpvoted()))
  async def meme(self,ctx):
  



    subreddits = ['https://www.reddit.com/r/dankmemes/new.json?sort=hot','https://www.reddit.com/r/okbuddyretard/new.json?sort=hot','https://www.reddit.com/r/memes/new.json?sort=hot',
    'https://www.reddit.com/r/wholesomememes/new.json?sort=hot', 'https://www.reddit.com/r/meme/new.json?sort=hot', 'https://www.reddit.com/r/PrequelMemes/new.json?sort=hot','https://www.reddit.com/r/deepfriedmemes/new.json?sort=hot', 'https://www.reddit.com/r/nukedmemes/new.json?sort=hot']
    async with aiohttp.ClientSession() as cs:
      async with cs.get(subreddits[random.randint(0,len(subreddits))]) as r:
        res = await r.json()
        randomn = random.randint(0,15)
        color = int(await colorSetup(ctx.message.author.id),16)
        embed = discord.Embed(color = color,title = res['data']['children'] [randomn]["data"]["title"])
        
        embed.set_image(url=res['data']['children'] [randomn]['data']['url'])
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
    try:
      if users[str(user.id)]["deletedMessage"]=='':
        await ctx.reply("There's nothing to snipe!")
        raise Exception
      if settings[str(user.id)]["sniped"] == 0:
        await ctx.reply("This guy can't be sniped, what a loser.")
      else:
            
        color = int(await colorSetup(ctx.author.id),16)
        embed = discord.Embed(color= color,description=users[str(user.id)]["deletedMessage"])        
        embed.set_footer(text="UTC "+users[str(user.id)]["date"])
      
        embed.set_author(name= f"{user.name}", icon_url = user.avatar_url)
        tip = postTips()
        
        if tip != None:
          
          await ctx.send(tip)
        await ctx.send(embed=embed)
        return
    except:
      pass

      
      

def setup(bot):
    bot.add_cog(Misc(bot))