import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import os 
from other.asyncCmds import colorSetup, addData ,addDataU,getDataU,postTips
import random
import json
import asyncio
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType,Select,SelectOption
from other.customCooldown import CustomCooldown
from other.upvoteExpiration import getUserUpvoted

class Setups(commands.Cog):
  
  def __init__(self, bot):
        self.bot = bot

  
  @commands.command(name = "credits",aliases = ["vote","invite"])
  async def credit(self,ctx):
    guilds = len(self.bot.guilds)
    username = await self.bot.fetch_user(int(os.environ['uid']))
    color = int(await colorSetup(ctx.message.author.id),16)
    embedVar3 = discord.Embed(color = color)
    embedVar3.add_field(name = "Annoybot 1.6.1", value = "Done by " +str(username)+"\n[Invite link](https://discord.com/api/oauth2/authorize?client_id=844757192313536522&permissions=4294967287&scope=bot)\n[dbl link](https://discordbotlist.com/bots/annoybot-4074)\n[top.gg link](https://top.gg/bot/844757192313536522)\n[support server](https://discord.gg/UCGAuRXmBD)\nServer count: "+ str(guilds),inline = False)
    await ctx.send(embed = embedVar3)

  #------------------------------------------
  @commands.command(name = "cmds", aliases = ["commands","cmd","help"])
  async def pages(self,ctx):
    

    color = int(await colorSetup(ctx.message.author.id),16)
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


    embedVar6 = discord.Embed(color = color)
    embedVar6.set_author(name="Annoybot commands (setup)")
    embedVar6.add_field(name = "``patchnotes``", value = "Shows the latest patch notes!",inline = False)
    embedVar6.add_field(name = "``settings (*option, *value)``", value = "Shows user settings. ",inline = False)
    embedVar6.add_field(name = "``changeprefix (prefix)``", value = "Changes the bot's prefix in the server.",inline = False)
    embedVar6.add_field(name = "``vote``", value = "Sends links to support this bot!",inline = False)

    paginationList = [embedVar,embedVar2,embedVar3,embedVar4,embedVar5,embedVar6]
    
    current = 0
    tip = postTips()
        
    if tip != None:
      await ctx.send(tip)
    await ctx.send("The values in brackets are additional arguments you're supposed to give. * denotes an optional argument.")
    mainMessage = await ctx.reply(
        
        embed = paginationList[current],
        components = [ 
          Select(placeholder="Other pages", options=[SelectOption(label="Main features", value="0"), SelectOption(label="Math", value="1"), SelectOption(label="Misc", value="2"), SelectOption(label="Trolls", value="3"), SelectOption(label="Games", value="4"), SelectOption(label="Setup", value="5")])
        ]
    )
    
    while True:
        
        try:
            interaction = await self.bot.wait_for(
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
            

  #-------------------end
  @commands.command(pass_context=True)
  @has_permissions(administrator=True) 
  async def changeprefix(self,ctx, prefix):
      await addData(ctx.guild.id)
      with open('./json/serverData.json', 'r') as f:
          prefixes = json.load(f)

      d = {"Prefix" : prefix}
      prefixes[str(ctx.guild.id)].update(d)



      with open('./json/serverData.json', 'w') as f:
          json.dump(prefixes, f)

      await ctx.send(f'Prefix changed to: {prefix}')

  @commands.command()
  async def settings(self,ctx, option = None, arg = None):

  
  
    uid = ctx.message.author.id

    await addDataU(uid)
    
    users = await getDataU()
    
    colors = ["red","yellow",'blue','green','magenta','purple','brown','black']
    hexCodes = ["ff0000",'ffff00','0000ff','00ff00','ff00ff','800080','964b00','000000']
    onoff = ["off",'on']
    

    try:
      if option.lower() == "color":
        if arg.lower() in colors:
          code = hexCodes[colors.index(arg.lower())]
          await addDataU(uid)
          users = await getDataU()
        
          d = {"color" : code}
          users[str(uid)].update(d)

          with open("./json/userSettings.json","w") as f:
            json.dump(users,f)
          await ctx.send("Embed color is now **"+colors[hexCodes.index(users[str(uid)]["color"])]+"**")
          
        elif arg.lower() != "off" and arg.lower() != "disable" and arg.lower() != "on" and arg.lower() != "enable":
          
          await ctx.send("You're missing an argument: ``value`` in that command, dumbass.")

      if option.lower() == "familyfriendly":
        
        if arg.lower() == 'on' or arg.lower() == 'enable':
          
          await addDataU(uid)
          users = await getDataU()
        
          d = {"familyFriendly" : 1}
          users[str(uid)].update(d)

          with open("./json/userSettings.json","w") as f:
            json.dump(users,f)
          await ctx.send("Family friendly mode is now **on**.")

        if arg.lower() == 'off' or arg.lower() == 'disable':
          
          await addDataU(uid)
          users = await getDataU()
        
          d = {"familyFriendly" : 0}
          users[str(uid)].update(d)

          with open("./json/userSettings.json","w") as f:
            json.dump(users,f)
          await ctx.send("Family friendly mode is now **off**.")
          
        elif arg.lower() != "off" and arg.lower() != "disable" and arg.lower() != "on" and arg.lower() != "enable":
          
          await ctx.send("You're missing an argument: ``value`` in that command, dumbass.")




      if option.lower() == "sniped":
        
        if arg.lower() == 'on' or arg.lower() == 'enable':
          
          await addDataU(uid)
          users = await getDataU()
        
          d = {"sniped" : 1}
          users[str(uid)].update(d)

          with open("./json/userSettings.json","w") as f:
            json.dump(users,f)
          await ctx.send("The ability to be sniped is now **on**.")

        if arg.lower() == 'off' or arg.lower() == 'disable':
          
          await addDataU(uid)
          users = await getDataU()
        
          d = {"sniped" : 0}
          users[str(uid)].update(d)

          with open("./json/userSettings.json","w") as f:
            json.dump(users,f)
          await ctx.send("The ability to be sniped is now **off**.")
          
        elif arg.lower() != "off" and arg.lower() != "disable" and arg.lower() != "on" and arg.lower() != "enable":
          
          await ctx.send("You're missing an argument: ``value`` in that command, dumbass.")
      if option == "dmblocker":
        if arg.lower() == "on" or arg.lower() == "enable":
          await addDataU(uid)
          users = await getDataU()
          try:
            d = {"dmblocker" : 1}
            users[str(uid)].update(d)

            with open("./json/userSettings.json","w") as f:
              json.dump(users,f)
            await ctx.send("DM-blocker is now **on**.")
          except KeyError:
            users[str(uid)]["dmblocker"] = 1
            with open("./json/userSettings.json","w") as f:
              json.dump(users,f)
            await ctx.send("DM-blocker is now **on**.")
        if arg.lower() == "off" or arg.lower() == "disable":
          await addDataU(uid)
          users = await getDataU()
          try:
            d = {"dmblocker" : 0}
            users[str(uid)].update(d)

            with open("./json/userSettings.json","w") as f:
              json.dump(users,f)
            await ctx.send("DM-blocker is now **off**.")
          except KeyError:
            users[str(uid)]["dmblocker"] = 0
            with open("./json/userSettings.json","w") as f:
              json.dump(users,f)
            await ctx.send("DM-blocker is now **off**.")
        elif arg.lower() != "off" and arg.lower() != "disable" and arg.lower() != "on" and arg.lower() != "enable":
          
          await ctx.send("You're missing an argument: ``value`` in that command, dumbass.")
    except:
        pass
  
      
      
    if option == None:
        
      colorDisp = colors[hexCodes.index(users[str(uid)]["color"])]
      color = int(await colorSetup(ctx.message.author.id),16)
      
      em = discord.Embed(color = color)
      em.set_author(name = 'Annoybot User Settings')
      em.add_field(name = "Preferred embed colour (color)",value = "Current: **"+colorDisp +"**\nChanges the colour of embed sent through the bot to a specific colour. Options are ``red``, ``yellow``, ``blue``, ``green``, ``magenta``, ``purple``, ``brown``, ``black``" ,inline= False)
      em.add_field(name = "Family Friendly (familyFriendly)",value = "Current: **"+onoff[users[str(uid)]["familyFriendly"]] +"**\nCensors some swear words. Options are ``on`` or ``off``" ,inline= False)
      em.add_field(name = "Can be sniped (sniped)",value = "Current: **"+onoff[users[str(uid)]["sniped"]] +"**\nDetermines if you can me sniped by others.\nOptions are ``on`` or ``off``" ,inline= False)
      em.add_field(name = "Can be dm'ed (dmblocker)",value = "Current: **"+onoff[users[str(uid)]["dmblocker"]] +"**\nDetermines if you can be dm'ed by the bot.\nOptions are ``on`` or ``off``" ,inline= False)
      await ctx.send(embed =em)
    


  @commands.command()
  async def ping(self,ctx):
     await ctx.send(f'Pong!\nPing: {round(self.bot.latency * 1000)}ms')

def setup(bot):
    bot.add_cog(Setups(bot))