import discord
from discord.ext import commands
import math
import numexpr
import json
from other.asyncCmds import colorSetup,postTips
from other.customCooldown import CustomCooldown
from other.upvoteExpiration import getUserUpvoted


class Math(commands.Cog):
  
  def __init__(self, bot):
        self.bot = bot

  @commands.command()
  @commands.check(CustomCooldown(1, 10, 1, 5, commands.BucketType.user, elements=getUserUpvoted()))
  async def calc(self,ctx,*args):
    question = ''
    for arg in args:
      question = question +arg
    
    try:
      CONST = {"pi": math.pi, "e": math.e}
      result = numexpr.evaluate(str(question), CONST)
    except:
      await ctx.reply("The inputs are supposed to be NUMBERS, ya braindead vegetable.")
      
    

    question = question.replace("**","^").replace("/","\u00F7").replace("pi","\u03C0").replace("*","\u00D7")
    
          

    
          
    color = int(await colorSetup(ctx.message.author.id),16)
    embedVar5 = discord.Embed(color = color)
    embedVar5.set_author(name="Requested by"+' {}'.format(ctx.message.author), icon_url = ctx.message.author.avatar_url)
    embedVar5.add_field(name = "Input", value = question,inline = False)
    embedVar5.add_field(name = "Result", value = "```py\n" + str(result)+"```",inline = False)
    await ctx.send(embed=embedVar5)


  @commands.command()
  @commands.check(CustomCooldown(1, 10, 1, 5, commands.BucketType.user, elements=getUserUpvoted()))
  async def form(self,ctx,operator,*args):
    argList = []
    for arg in args:
      if arg.isdigit() == False:
        await ctx.send("The inputs are supposed to be NUMBERS, ya braindead vegetable.")
      else:
        argList.append(arg)

    result =""

    question=""


    def convert_to_float(frac_str):
          try:
            return float(frac_str)
          except ValueError:
            num, denom = frac_str.split('/')
            
            frac = float(num) / float(denom)
            return frac 
    def circleArea(x):
      x= convert_to_float(x)
      return math.pi*(x**2)
    def circleCircum(x):
      x= convert_to_float(x)
      return 2*math.pi*x
    def triangleArea(x,y):
      x= convert_to_float(x)
      y= convert_to_float(y)
      return 0.5*x*y
    def pythagoras(x,y):
      x= convert_to_float(x)
      y= convert_to_float(y)
      return math.sqrt((x**2)+(y**2))
    def spherevol(x):
      x= convert_to_float(x)
      
      return 4*(math.pi*(x**3))/3


    if operator.lower() == "circlearea":
      question = '```py\n\u03c0('+ argList[0] + '²)```'
      result = circleArea(argList[0])
    if operator.lower() == "circlecircum":
      question = '```py\n2\u03c0'+ argList[0] + '```'
      result = circleCircum(argList[0])
    if operator.lower() == "spherevol":
      question = '```py\n4/3*\u03c0*'+ argList[0] + '³```'
      result = spherevol(argList[0])
    if operator.lower() == "spherearea":
      question = '```py\n4\u03c0'+ argList[0] + '²```'
      result = 4*circleArea(argList[0])
    if operator.lower() == "trianglearea":
      
      if len(argList) < 2:
        await ctx.send("You need a second value for this command.")
      else:
        question = '```py\n\u00BD'+ argList[0] +"\u2715" + argList[1]+'```'
        result = triangleArea(argList[0],argList[1])
    if operator.lower() == "pythagoras":
      
      if len(argList) < 2:
        await ctx.send("You need a second value for this command.")
      else:
        question = 'Solve for x:\n```py\nx² = '+ argList[0] +"² + " + argList[1]+'²```'
        result = pythagoras(argList[0],argList[1])
    else:
      await ctx.send("You need a valid operator to calculate your result.")
        

    
    color = int(await colorSetup(ctx.message.author.id),16)
    embedVar5 = discord.Embed(color = color)
    embedVar5.set_author(name="Requested by"+' {}'.format(ctx.message.author), icon_url = ctx.message.author.avatar_url)
    embedVar5.add_field(name = "Input", value = question,inline = False)
    embedVar5.add_field(name = "Result", value = "```py\n" + str(result)+"```",inline = False)
    tip = postTips()
        
    if tip != None:
          
      await ctx.send(tip)
    await ctx.send(embed=embedVar5)
      







def setup(bot):
    bot.add_cog(Math(bot))