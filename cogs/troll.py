import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import os 
from other.asyncCmds import colorSetup,addData,getDataU,addDataU,postTips
import random
import json
import asyncio
import string
from other.customCooldown import CustomCooldown
from other.upvoteExpiration import getUserUpvoted
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType,Select,SelectOption

class Troll(commands.Cog):
  
  def __init__(self, bot):
        self.bot = bot

        
  
  @commands.command()
  @commands.check(CustomCooldown(1, 10, 1, 5, commands.BucketType.user, elements=getUserUpvoted()))
  @commands.bot_has_guild_permissions(manage_channels=True)
  async def channeltroll(self,ctx,user: discord.Member = None):
    if user:
      
      randomstr = ''.join(random.choices(string.ascii_lowercase+string.digits,k=10))
      trolledUser = user
      
      
      guild = ctx.guild
      
      overwrites = {
          guild.default_role: discord.PermissionOverwrite(read_messages=False),
          guild.me: discord.PermissionOverwrite(read_messages=True),
          trolledUser: discord.PermissionOverwrite(read_messages=True)
          
      }
      await guild.create_text_channel(randomstr, overwrites=overwrites)
      for channel in ctx.guild.channels:
          if channel.name == randomstr:
            channel_id = channel.id


      tip = postTips()
        
      if tip != None:
          
        await ctx.send(tip)
      await ctx.send(f"A new channel {channel.mention} was created. The bot will ping the trolled user 3 times to annoy them.")
      
          
      
      
      channel = self.bot.get_channel(channel_id)
      
      def response(m):
          return m.author == user

      while True:   
        try:
          for i in range(3):
            await channel.send(user.mention+" you've been trolled")
            await asyncio.sleep(0.5)
            
          response = await self.bot.wait_for('message', check=response, timeout=120.0)
          await channel.send(ctx.author.mention+" trolled you lol.")
          await asyncio.sleep(1)
          existing_channel = discord.utils.get(guild.channels, name=randomstr)
    
    
          if existing_channel is not None:
            await existing_channel.delete()
        
          

        except asyncio.TimeoutError:
          existing_channel = discord.utils.get(guild.channels, name=randomstr)
    
    
          if existing_channel is not None:
            await existing_channel.delete()
        break


  
  @commands.command()
  @commands.check(CustomCooldown(1, 10, 1, 5, commands.BucketType.user, elements=getUserUpvoted()))
  @commands.bot_has_guild_permissions(manage_nicknames=True)
  async def nicktroll(self,ctx, member: discord.Member, *args):
    if member:
      bot_member = ctx.guild.get_member(self.bot.user.id)
      if bot_member.top_role <= member.top_role:
        await ctx.send("Can't do that, that member's top role is higher than mine.")
      else:
        if not args:
          nick = ''.join(random.choices(string.ascii_letters+string.digits,k=10))
        
        else:
          nick = ''
          for arg in args:

            nick = nick + ' ' + arg
          
          
        await member.edit(nick=nick)
        tip = postTips()
        
        if tip != None:
          
          await ctx.send(tip)
        await ctx.send(f'Nickname was changed for {member} to **{nick}** for 5 minutes. ')
        await asyncio.sleep(300.0)
        await member.edit(nick=None)

      

  @commands.command()
  @commands.check(CustomCooldown(1, 10, 1, 5, commands.BucketType.user, elements=getUserUpvoted()))
  async def dmtroll(self,ctx, user : discord.Member):
    uid = user.id
    users = await getDataU()
    


    async def command():
      tip = postTips()
        
      if tip != None:
          
        await ctx.send(tip)
      
      channel = await user.create_dm()
      
      for i in range(3):
        await channel.send(user.mention + " imagine getting pinged in DMs moron.")
      await channel.send(f"Dmtroll from {ctx.author.name} in {ctx.guild.name}")
      
      
      
      
    try:
      if users[str(uid)]["dmblocker"] == 0:
        await ctx.send("The trolled user will be pinged 3 times through dms lol.")
        
        await command()
        

        
      elif users[str(uid)]["dmblocker"] ==1:
        await ctx.send("Sorry, the user you mentioned doesn't want to be dm'ed by me ;(")

      
    except KeyError:
      await addDataU(uid)
      users[str(uid)]["dmblocker"] = 0
      with open("./json/userSettings.json","w") as f:
        json.dump(users,f)
      await ctx.send("The trolled user will be pinged 3 times through dms lol.")
      await command()

      

  
  @commands.command()
  @commands.check(CustomCooldown(1, 10, 1, 5, commands.BucketType.user, elements=getUserUpvoted()))
  async def ghosttroll(self,ctx,user: discord.Member):
    


    allowedChannels = []
    
    for channel in ctx.guild.channels:
      if user.permissions_in(channel).send_messages and str(channel.type) ==  'text':
        
        allowedChannels.append(channel.id)

    if len(allowedChannels) != 0:
      await ctx.send("The user will be ghost pinged in 3 channels to annoy them.")   
    else: 
      await ctx.send("That user can't access any channels, dummy.")  

    i = 3
    while True:
      
      try:
        targetChannel = self.bot.get_channel(allowedChannels[random.randint(0,len(allowedChannels))])
        
          
        message = await targetChannel.send("{}".format(user.mention))
        await asyncio.sleep(0.1)
        await message.delete()
        i-=1
        await asyncio.sleep(1)
        if i == 0:
          break

      except Exception:
        pass

  

  @commands.command()
  @commands.check(CustomCooldown(1, 10, 1, 5, commands.BucketType.user, elements=getUserUpvoted()))
  async def fakemute(self,ctx,user: discord.Member,*args):
    

    reason = ""
    msg = ""
    for arg in args:
      msg =msg + arg
    if msg == "":
      reasons = ["Too annoying in chat.", "Rolled the Rick.", "Having an opinion.","Needing help.","Farting in vc","Breaking rule no. class 'c' section 'f' rule '12-02'. ","Being the alpha male","wearing a condom and livestreaming it."]
      reason = reasons[random.randint(0,len(reasons)-1)]
    else:
      for arg in args:
        reason = reason + " "+ arg
    color = int(await colorSetup(ctx.message.author.id),16)
    em = discord.Embed(color =  color)
    
    em.add_field(name="**mute**",value="**Offender:** {}".format(user.mention)+"\n**Reason:** "+reason+"\n**Responsible mod:** {}".format(ctx.author),inline=False)

    em.set_footer(text="sike you thought")
              
              
    tip = postTips()
        
    if tip != None:
          
      await ctx.send(tip)
    await ctx.send(embed=em)

  
  @commands.command()
  @commands.check(CustomCooldown(1, 10, 1, 5, commands.BucketType.user, elements=getUserUpvoted()))
  
  @commands.bot_has_guild_permissions(create_instant_invite=True,kick_members=True)
  @has_permissions(kick_members = True)
  async def fakeban(self,ctx,user: discord.Member):
    
    
    await ctx.send("This command will only KICK the member, but not ban them. Are you sure you want to continue?\n`yes` or `no`")
    channel = await user.create_dm()
    def check(msg):
      return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ['yes','no']
    try:
      msg = await self.bot.wait_for("message",timeout=30,check=check)
      if msg.content == "yes":
        try:
          invite = await ctx.channel.create_invite(max_uses=1,unique=True)
          msg_1=await channel.send(f"You've been 'banned' from {user.guild.name} \nlmfao get trolled by {ctx.author.name}")
          msg_2=await channel.send(str(invite))
          await user.kick()
          await ctx.send("The user has been kicked and sent an invite.")
        except:
          await ctx.send("Sorry, that user's top role is higher than mine, so I can't kick them.")
          await self.bot.http.delete_message(channel.id, msg_1.id)
          await self.bot.http.delete_message(channel.id, msg_2.id)
          await channel.send(f"LOL {ctx.author.name} tried to troll you but failed.")
      if msg.content == "no":
        await ctx.send("ok, cancelled.")
    except asyncio.TimeoutError:
      await ctx.send("ok, cancelled.")

  @commands.command(pass_context = True)
  @commands.check(CustomCooldown(1, 10, 1, 5, commands.BucketType.user, elements=getUserUpvoted()))
  @commands.bot_has_guild_permissions(manage_messages=True)
  async def nitrotroll(self,ctx):
    await ctx.message.delete()
    em = discord.Embed(color = 0x000000, title = "A wild gift appears!", description = "Nitro classic (3 months)\nThis link will expire in 12 hours, claim it now!").set_thumbnail(url ="https://i.imgur.com/w9aiD6F.png")
    msg = await ctx.send("https://dicsord.com/gifts/get9troll3d5you2m0r0n",embed = em, components = [ 
              [
                  Button(
                      label = "\ufeff\ufeff\ufeff\ufeff\ufeff\ufeffClaim\ufeff\ufeff\ufeff\ufeff\ufeff\ufeff",
                      id = "claim",
                      style = ButtonStyle.green
                      
                      
                  )]])
    interaction = await self.bot.wait_for("button_click",check = lambda i: i.component.id == "claim", timeout = None)
    await msg.edit(
    embed = discord.Embed(color = 0x000000, title = "You received a gift, but...", description = "The gift link has either expired or has been revoked.\nThe sender can still create a new link to send again.").set_thumbnail(url ="https://i.imgur.com/w9aiD6F.png"),components = [ 
              [
                  Button(
                      label = "\ufeff\ufeff\ufeff\ufeff\ufeffClaimed\ufeff\ufeff\ufeff\ufeff\ufeff",
                      id = "claim",
                      style = ButtonStyle.grey,
                      disabled = True
                      
                  )]])

    await interaction.respond(type=4, content="You idiot lol\nhttps://c.tenor.com/x8v1oNUOmg4AAAAd/rickroll-roll.gif", ephemeral=True)

    
def setup(bot):
    bot.add_cog(Troll(bot))