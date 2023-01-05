import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import has_permissions
from typing import *

from other.asyncCmds import colorSetup,addData,getDataU,addDataU,postTips

import random
import asyncio
import string
import datetime





class Troll(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot

        

  
  @app_commands.command(name = "channeltroll", description="Creates a temporary thread then pings a user once to mess with them")
  @app_commands.describe(user="The user to ping")
  @app_commands.checks.bot_has_permissions(send_messages_in_threads = True, create_public_threads=True, manage_threads = True)
  @app_commands.guild_only()
  async def channeltroll(self, interaction: discord.Interaction, user: discord.Member):
    
    addDataU(user.id)
    randomstr = ''.join(random.choices(string.ascii_lowercase+string.digits,k=10))
    if isinstance(interaction.channel, discord.abc.GuildChannel):
      channel = await interaction.channel.create_thread(name = randomstr, auto_archive_duration =1440)
    elif isinstance(interaction.channel, discord.Thread):
       channel = await interaction.channel.parent.create_thread(name = randomstr, auto_archive_duration =1440)
    else:
      raise Exception("exception in channeltroll: channel is unknown")

      

    await interaction.response.send_message(f"A new thread {channel.mention} was created. The bot will ping this user to annoy them.")
      
          
      
    message = [
      "We would like to contact you about your car's extended warranty.",
      "You have a virus on your computer, call Microsoft Support at +91 6969 6969",
      "Early incidents of trolling were considered to be the same as flaming, but this has changed with modern usage by the news media to refer to the creation of any content that targets another person. The Internet dictionary, NetLingo, suggests there are four grades of trolling: playtime trolling, tactical trolling, strategic trolling, and domination trolling. The relationship between trolling and flaming was observed in open-access forums in California, on a series of modem-linked computers.",
      "早上好中国，我喜欢bing chilling",
      "Suck on your dad",
      "Hiya, we would like you to join us on mission to prove the earth is flat",
      "🤓",
      "Good evening sir, how would you like your coffee done today?",
      "Hello, we have an arrest warrant for joe? Are you Joe?"
    ]
     
       
    try:
      
      await channel.send(f"Hello, {user.mention}. {random.choice(message)}")
      
            
      await self.bot.wait_for('message', check= lambda m: m.author == user and m.channel == channel, timeout = 180)
      await channel.send(f"courtesy of {interaction.user.mention}. this thread has been automatically archived, but you can keep it around if you'd like")
      await asyncio.sleep(1)
      
          

    except asyncio.TimeoutError:
      pass
    finally:
      await channel.edit(archived = True)
    



  
  @app_commands.command(name = "nicktroll", description = "Generates a temporary nickname for a user")
  @app_commands.checks.bot_has_permissions(manage_nicknames = True)
  @app_commands.describe(member="The member to troll", name = "A nick to give")
  async def nicktroll(self, interaction: discord.Interaction, member: discord.Member, name: Optional[str]=None):
    addDataU(member.id)
    bot_member = interaction.guild.get_member(self.bot.user.id)
    if bot_member.top_role <= member.top_role or member == interaction.guild.owner:
      await interaction.response.send_message("❌ Can't do that, that member's top role is either equal to or higher than my top role.")
    else:
      if not name:
         name = ''.join(random.choices(string.ascii_letters+string.digits,k=10))
        
      
        
          
      await member.edit(nick=name)

        

      await interaction.response.send_message(f'Nickname was changed for {member} to **{name}** for 3 minutes. ')
      await asyncio.sleep(180.0)
      await member.edit(nick=None)

      


  @app_commands.command(name = "dmtroll", description = "pings a user in DMs once")
  @app_commands.describe(user="The user to ping")
  @app_commands.guild_only()
  async def dmtroll(self, interaction: discord.Interaction, user : discord.Member):
    addDataU(user.id)
    if bool(getDataU(user.id).get("dmblocker")) or user.bot:
      await interaction.response.send_message(content="❌ The user you mentioned is either a bot, or does not want to be DM'ed. Bet you look stupid now.", ephemeral=True)
      return 
  
    channel = await user.create_dm()
      
    try:
      await channel.send(f"{user.mention} hey 😏, did u like the ping sound?\n/dmtroll from {interaction.user.display_name} in {interaction.guild.name}")
    except:
      await interaction.response.send_message("❌ The user blocked this bot from sending messages to them, lol pussy")
      
      
      
      
    
    await interaction.response.send_message("The trolled user has been pinged through dms lol.")
      
        
        

      

  
  @app_commands.command(name = "ghosttroll", description = "Ghostpings a user in 3 different channels")
  @app_commands.describe(user="The user to ping")
  @app_commands.guild_only()
  async def ghosttroll(self, interaction: discord.Interaction ,user: discord.Member):
    


    allowedChannels = []
    
    for channel in interaction.guild.channels:
      if channel.permissions_for(user).send_messages and str(channel.type) ==  'text':
        
        allowedChannels.append(channel.id)

    if len(allowedChannels) != 0:
      await interaction.response.send_message("The user will be ghost pinged in 3 channels to annoy them.")   
    else: 
      await interaction.response.send_message("That user can't access any channels, bruh wtf")  

    i = 3
    while i !=0:
      
      try:
        targetChannel = self.bot.get_channel(random.choice(allowedChannels))
        
          
        message = await targetChannel.send("{}".format(user.mention))
        await asyncio.sleep(0.1)
        await message.delete()
        i-=1
        await asyncio.sleep(1)
        

      except Exception:
        continue


  

  @app_commands.command(name = "fakemute", description = "Fakes a mute for a user")
  @app_commands.describe(user="The user to 'mute'")
  @app_commands.guild_only()
  @app_commands.checks.bot_has_permissions(moderate_members = True)
  async def fakemute(self, interaction: discord.Interaction ,user: discord.Member, reason: Optional[str]=None):
    
    #check subset of permissions or role
    if interaction.guild.get_member(self.bot.user.id).top_role <= user.top_role or  user.guild_permissions.administrator:
      await interaction.response.send_message("❌ Can't do that, that member's top role is either equal to or higher than my top role.")
      return

    
    if not reason:
      reasons = ["Too annoying in chat.", "Rolled the Rick.", "Having an opinion.","Needing help.","Farting in vc","Breaking rule no. class 'c' section 'f' rule '12-02'. ","Being the alpha male","wearing a condom and livestreaming it."]
      reason = random.choice(reasons)
    
    color = colorSetup(interaction.user.id)
    em = discord.Embed(color =  color)
    
    em.add_field(name="**Mute**",value=f"**Offender:** {user.mention}\n**Reason:** {reason}\n**Responsible mod:** {interaction.user.display_name}",inline=False)

    em.set_footer(text="imagine")

    await user.timeout(datetime.timedelta(seconds= 3))
              
    
    await interaction.response.send_message(embed=em)

  
  @app_commands.command(name = "fakeban", description = "Fakes a ban for a user")
  @app_commands.describe(user="The user to 'ban'")
  @app_commands.guild_only()
  @app_commands.checks.bot_has_permissions(moderate_members = True, manage_nicknames=True)
  async def fakeban(self, interaction,user: discord.Member):
    color = colorSetup(interaction.user.id)
    em = discord.Embed(color =  color)
    
    em.add_field(name="**Ban**",value=f"**Offender:** {user.mention}\n**Responsible mod:** {interaction.user.display_name}",inline=False)

    em.set_footer(text="imagine")
    await interaction.response.send_message(embed=em)
    await asyncio.sleep(0.1)
    await user.edit(nick=f'!<{user.id}>')
    await user.timeout(datetime.timedelta(seconds= 3))
    try:
      await self.bot.wait_for('message', check= lambda m: m.author == user, timeout = 180)
    except asyncio.TimeoutError:
      pass
    finally:
      await user.edit(nick=None)
    
    
    
  @app_commands.command(name = "nitrotroll", description = "Sends a fake nitro embed")
  async def nitrotroll(self, interaction: discord.Interaction):
    em = discord.Embed(color = 0x7289da, title = "A wild gift appears!", description = "Nitro classic (3 months)\nThis link will expire in 12 hours, claim it now!").set_thumbnail(url ="https://i.imgur.com/w9aiD6F.png")
    
    class claim(discord.ui.View):
      def __init__(self):
        super().__init__()

      @discord.ui.button(label="Claim", style=discord.ButtonStyle.green)
      async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.style = discord.ButtonStyle.grey
        button.disabled = True
        em = discord.Embed(color = 0x000000, title = "You received a gift, but...", description = "The gift link has either expired or has been revoked.\nThe sender can still create a new link to send again.").set_thumbnail(url ="https://i.imgur.com/w9aiD6F.png")
        await interaction.response.edit_message(embed = em, view=self)
        await interaction.followup.send(content="You idiot lol\nhttps://c.tenor.com/x8v1oNUOmg4AAAAd/rickroll-roll.gif", ephemeral=True)
        
    await interaction.response.send_message(content=".")
    msg = await interaction.original_response()
    await msg.delete()
    await interaction.channel.send(content = "https://dicsord.com/gifts/get9troll3d5you2m0r0n", embed = em, view = claim())

    
async def setup(bot):
  await bot.add_cog(Troll(bot))

