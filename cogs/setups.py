import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import os 
from other.utilities import colorSetup ,addDataU,getDataU, postTips, getData, addData, bool_to_int
from discord import app_commands
from typing import List
import json
import asyncio
import re
from typing import *
import other.userSettings as userSettings
import asyncio

import datetime
import other.serverSettings as serverSettings

class Setups(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot

    
    
  @app_commands.command(name = "info", description="Shows general information and support links.")
  async def credit(self, interaction: discord.Interaction):
    view = discord.ui.View() 
    guilds = str(len(self.bot.guilds))
    username = await self.bot.fetch_user(int(os.environ['uid']))
    color = colorSetup(interaction.user.id)

    
    embedVar3 = discord.Embed(color = color)
    embedVar3.add_field(name = "Annoybot 1.9.0", value = f"""Developed by {str(username)}
    Library: discord.py 2.2.2
    [invite link](https://discord.com/api/oauth2/authorize?client_id=844757192313536522&permissions=1507264163186&scope=applications.commands%20bot)\n
    Support us!!
    [top.gg](https://top.gg/bot/844757192313536522)
    [dbl link](https://discordbotlist.com/bots/annoybot-4074)
    [AYB link](https://ayblisting.com/bots/844757192313536522)
    Server count: {guilds}""",inline = False)

    
      
      
    

    class Info(discord.ui.View):
      def __init__(self):
        super().__init__()

      @discord.ui.button(label="Patch notes", style=discord.ButtonStyle.green)
      async def cl(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("hi")
        with open("./PATCHNOTES.txt", 'r') as patchnotes:
          em = discord.Embed(color = color, title = "1.9.0", description = patchnotes.read())
        await interaction.response.send_message(embed=em)

      @discord.ui.button(label="Terms of use", style=discord.ButtonStyle.primary)
      async def tos(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open("./legal_docs/terms_of_use.txt", 'r') as doc:
          em = discord.Embed(color = color, description = doc.read())
        await interaction.response.send_message(embed=em)

      @discord.ui.button(label="Privacy policy", style=discord.ButtonStyle.primary)
      async def privacy_pol(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open("./legal_docs/priv_policy.txt", 'r') as doc:
          em = discord.Embed(color = color, description = doc.read())
        await interaction.response.send_message(embed=em)

      @discord.ui.button(label="License", style=discord.ButtonStyle.primary)
      async def lic(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open("./legal_docs/LICENCE.txt", 'r') as doc:
          em = discord.Embed(color = color, description = doc.read())
        await interaction.response.send_message(embed=em)

    
    
    
    await interaction.response.send_message(embed = embedVar3, view= Info().add_item(discord.ui.Button(
        style=discord.ButtonStyle.link, 
        label="support server", 
        url="https://discord.gg/UCGAuRXmBD"
      )))




  
  @app_commands.command(name = "help", description = "Shows a list of commands that you can use")
  async def pages(self, interaction: discord.Interaction):
    color = colorSetup(interaction.user.id)
    def contents() -> List[discord.Embed]:
      
      embedVar = discord.Embed(color = color)
      embedVar.set_author(name="Annoybot commands")
      embedVar.add_field(name = "``roast (*user)``", value = "Give[s](<https://www.bit.ly/IqT6zt>) a random roast to a mentioned user. (40 possibilities)",inline = False)
      
      embedVar.add_field(name = "``insult (*user)``", value = "The bot will generate an insult.",inline = False)
      embedVar.add_field(name = "``urmom``", value = "Gives a random Ur Momma joke. (30 possibilities)",inline = False)
      embedVar.add_field(name = "``uninspire``", value = "Gives a random uninspirational quote. (23 possibilities).",inline = False)
      embedVar.add_field(name = "``dmthreaten (user, *customthreat)``", value = "The bot DMs a user and threaten them. (13 possibilities).",inline = False)
      embedVar.add_field(name = "``dadjoke``", value = "Sends a dad joke.",inline = False)
      
      embedVar.add_field(name = "``dumbdeath(user)``", value = "Creates a fictional dumb death for the meantioned user.",inline = False)
      embedVar.add_field(name = "``darkjoke``", value = "Sends a dark joke. (20 possibilities) Warning, some jokes may be insensitive.",inline = False)
  
      
      
  
      embedVar3 = discord.Embed(color = color)
      embedVar3.set_author(name="Annoybot commands (misc)")
      embedVar3.add_field(name = "``utils pick (list)``", value = "Randomly chooses from a list of arguments the user provides.",inline = False)
      embedVar3.add_field(name = "``utils predict (question)``", value = "Predicts the answer to a yes/no question.",inline = False)
      embedVar3.add_field(name = "``autoresponse menu/add/remove/resetdb``", value = "Responds to certain keywords guild-wide and sends a message in return. \nRequires user to have **manage_server** permission.",inline = False)
      embedVar3.add_field(name = "``textwall(num,content,*tts)``", value = "Sends a wall of text up to 2000 characters.",inline = False)
      embedVar3.add_field(name = "``meme``", value = "Sends a meme from reddit",inline = False)
      embedVar3.add_field(name = "``copypasta``", value = "Sends a copypasta from r/copypasta.",inline = False)
      embedVar3.add_field(name = "``snipe (user)``", value = "Shows a user's recently deleted message.",inline = False)
      embedVar3.add_field(name = "``anime (type)``", value = "Shows a picture of an anime girl.",inline = False)
      embedVar3.add_field(name = "``iplookup(ip)``", value = "Looks up somebody's ip LOL.",inline = False)
      embedVar3.add_field(name = "``urbandict(text)``", value = "looks for the definition of the given word on urban dictionary.",inline = False)
      
  
      embedVar4 = discord.Embed(color = color)
      embedVar4.set_author(name="Annoybot commands (trolls)")
      
      embedVar4.add_field(name = "``channeltroll (user)``", value = "Creates a private thread and pings the trolled user 3 times. When either the trolled user speaks in the channel or 2 minutes have passed, the thread is archived.\nRequires bot to have **send_messages_in_threads, create_public_threads,  manage_threads** permissions.",inline = False)
      embedVar4.add_field(name = "``nicktroll (user,*threat)``", value = "Changes the nickname of a user temporarily to either a random set of characters or a chosen nickname.\nRequires bot to have **manage_nicknames** permission.",inline = False)
      embedVar4.add_field(name = "``nicktroll (user,name, *colour)``", value = "Gives the user a temporary role with a name and an optional colour provided/generated.\nRequires bot to have **manage_roles** permission.",inline = False)
      embedVar4.add_field(name = "``dmtroll (user)``", value = "Ping the affected user 3 times in their dms, then deletes it.",inline = False)
  
      embedVar4.add_field(name = "``ghosttroll (user)``", value = "Ghost pings the user in 3 different channels.",inline = False)
      embedVar4.add_field(name = "``roletroll (user, name, *colour)``", value = "Creates a new temporary unique role with a shitty name and colour for the user.\nRequires bot to have **manage_roles** permission.",inline = False)
      
  
      embedVar4.add_field(name = "``fakeban (user)``", value = "Times out a user for 2s, nicks them to their id (to give the illusion of being banned) and sends a fake ban reason.\nRequires bot to have **moderate_members, manage_nicknames** permission.",inline = False)
  
      embedVar4.add_field(name = "``fakemute (user,*reason)``", value = "Fakes a mute for the trolled user, timing them out for 2s. If no reason is given, a random one will be generated. \nRequires bot to have **moderate_members** permission.",inline = False)
      embedVar4.add_field(name = "``nitrotroll``",value = "Fakes a nitro gift in chat. Clicking on claim will produce a rickroll. Requires **manage_messages** permissions.")
      
      embedVar5 = discord.Embed(color = color)
      embedVar5.set_author(name="Annoybot commands (games)")
      embedVar5.add_field(name = "``memorygame``", value = "Memorise the pattern shown at the start of the level and try to replicate it from memory afterward.",inline = False)
      embedVar5.add_field(name = "``tictactoe (user)``", value = "Play tictactoe with a friend!",inline = False)
      embedVar5.add_field(name = "``vocabularygame``",value = "Test your vocabulary skills with this game! Requires bot to have **add_reaction** permission.", inline = False)
      embedVar5.add_field(name = "``typingrace``",value = "Race with others and see who can type the fastest!", inline = False)
      embedVar5.add_field(name = "``wouldyourather``",value = "Challenge your friends to a would you rather game. Best experienced in a VC!", inline = False)
      embedVar5.add_field(name = "``truthordare``", value = "Play a game of truth or dare with your friends. Best played in a VC or physically!", inline = False)
      
      embedVar6 = discord.Embed(color = color)
      embedVar6.set_author(name="Annoybot commands (setup)")
      embedVar6.add_field(name = "``settings (*option, *value)``", value = "Shows user settings. ",inline = False)
      embedVar6.add_field(name = "``info``", value = "Sends links to support this bot!",inline = False)
      embedVar6.add_field(name = "``resetdata``", value = "Resets and removes all your data from the bot.", inline = False)
      embedVar6.add_field(name = "``legal``", value = "Shows legal stuff. eh.", inline = False)
  
      embedVar7 = discord.Embed(color = color)
      embedVar7.set_author(name="Annoybot commands (voice)")
      embedVar7.add_field(name = "``earrape (*duration)``", value = "Joins your VC and plays a random earrape song",inline = False)
      embedVar7.add_field(name = "``playnoise fart``", value = "Plays a fart noise into your VC",inline = False)
      embedVar7.add_field(name = "``playnoise asmr``", value = "Plays a chewing noise into your VC",inline = False)
      embedVar7.add_field(name = "``playnoise cartoon``", value = "Plays a goofy cartoon noise into your VC",inline = False)
      embedVar7.add_field(name = "``playnoise indianinsult``", value = "Plays the voice of an indian dude insulting your cock into your VC. Credit: illiyasiya",inline = False)
      embedVar7.add_field(name = "``playnoise cbat``", value = "Plays cbat into your VC",inline = False)
      embedVar7.add_field(name = "``playnoise micblow``", value = "Plays a breathing/blowing noise into your VC",inline = False)
      embedVar7.add_field(name = "``playnoise scream``", value = "Plays a female screaming noise into your VC",inline = False)
      embedVar7.add_field(name = "``playnoise rickroll``", value = "Plays Never Gonna Give You Up (Rick Astley, 1987) into your VC",inline = False)

      embedVar8 = discord.Embed(color = color, description = "Right click on any message and navigate to apps>(command) to access these.")
      embedVar8.set_author(name="Annoybot commands (message)")
      embedVar8.add_field(name = "``'spam emojis'``", value = "Reacts to the selected message with random emojis",inline = False)
      embedVar8.add_field(name = "``'uwuify'``", value = "Transforms your message into a MeSsAgE",inline = False)
      
      embedVar8.add_field(name = "``'ratio'``", value = "Ratios someone's message for you",inline = False)
      

      return [embedVar,embedVar3,embedVar4,embedVar5,embedVar6,embedVar7,embedVar8]


    
    class options(discord.ui.Select):
      def __init__(self):
        options = [
          discord.SelectOption(label="Core features", description = "A list of features considered to be the main highlights.", emoji="🌌"),
          
          discord.SelectOption(label="Troll", description="Commands to troll your friends", emoji ="👺"),
          discord.SelectOption(label= "Voice", description="Commands used in voice channels to be annoying", emoji="🎤"),
          discord.SelectOption(label="Games", description="Games you can play with friends", emoji ="🎲"),
          discord.SelectOption(label="Misc", description="Contains some random features.", emoji="🌎"),
          discord.SelectOption(label="Setup", description = "Commands to aid in configuration of the bot", emoji = "⚙️"),
          discord.SelectOption(label="Message", description = "Commands modify/change messages", emoji = "💬")
        ]
        super().__init__(placeholder='Choose a category.', min_values=1, max_values=1, options=options)
      async def callback(self, interaction: discord.Interaction):
        view = discord.ui.View()
        view.add_item(item=options())
        value = self.values[0]
        
        pages = contents()
        get_page = {
          "Core features": pages[0],
          "Setup": pages[4],
          "Troll": pages[2],
          "Voice": pages[5],
          "Games": pages[3],
          "Misc": pages[1],
          "Message": pages[6]
          
        }
        
        await interaction.response.edit_message(embed= get_page.get(value), view = view)
        
    

    


    
    
    
    view = discord.ui.View()
    view.add_item(item=options())
    await interaction.response.send_message(content = "The values in brackets are additional arguments you're supposed to give.\n* denotes an optional argument.\nAll commands have a ratelimit of 10 commands per 30 seconds", embed = contents()[0], view = view )

    

  settings_group = app_commands.Group(name="settings", description="Shows your settings for the bot")
  
  
  @settings_group.command(name = "menu", description="Shows what your settings are")
  async def settings(self,interaction: discord.Interaction):
    
    settings = getDataU(interaction.user.id)
    
    color = colorSetup(interaction.user.id)
      
    em = discord.Embed(color = color)
    em.set_author(name = 'Annoybot User Settings')
    em.add_field(name = "Preferred embed colour (color)",value = f"Current: **#{settings.get('color')}**\nChanges the colour of embed sent through the bot to a specific colour." ,inline= False)
    em.add_field(name = "Family Friendly (familyfriendly)", value = f"Current: **{bool(settings.get('familyFriendly'))}**\nCensors some swear words. " ,inline= False)
    em.add_field(name = "Can be sniped (sniped)", value = f"Current: **{bool(settings.get('sniped'))}**\nDetermines if you can be sniped by others." ,inline= False)
    em.add_field(name = "Can be dm'ed (dmblocker)", value = f"Current: **{bool(settings.get('dmblocker'))}**\nIf true, this blocks incoming DMs from the bot, and sends an error message to anyone trying to DM you with the bot." ,inline= False)
    
    await interaction.response.send_message(embed =em, ephemeral=True)
    
  @settings_group.command(name = "color", description="Changes the default embed color. Enter a hex code as a color.")
  @app_commands.describe(color="The hex code of the color you want in your embeds.")
  async def color(self, interaction: discord.Interaction, color: app_commands.Range[str, 6, 6]):
    settings = getDataU(interaction.user.id)
    #validate
    if not re.search("^([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$", color):
      
      await interaction.response.send_message("❌ Enter a valid hex code, idiot.", ephemeral=True)
      return 
    settings['color'] = color
    userSettings.update(interaction.user.id, settings)
    await interaction.response.send_message(f"✅ Colour setting updated to **{color}**", ephemeral=True)
    
  @settings_group.command(name = "familyfriendly", description="Censors some swear words.")
  @app_commands.describe(onoff = "On or off")
  async def ff(self, interaction: discord.Interaction, onoff: bool):
    settings = getDataU(interaction.user.id)
    
    settings['familyFriendly'] = bool_to_int(onoff)
    userSettings.update(interaction.user.id, settings)
    await interaction.response.send_message(f"✅ familyfriendly setting updated to **{onoff}**", ephemeral=True)

  @settings_group.command(name = "sniped", description="Allows your messages to be stored to be sniped by /snipe")
  @app_commands.describe(onoff = "On or off")
  async def sniped(self, interaction: discord.Interaction, onoff: bool):
    settings = getDataU(interaction.user.id)
    
    settings['sniped'] = bool_to_int(onoff)
    userSettings.update(interaction.user.id, settings)
    await interaction.response.send_message(f"✅ sniped setting updated to **{onoff}**")
    
  @settings_group.command(name = "dmblocker", description="Blocks the bot from sending private messages to you.")
  async def dmblocker(self, interaction: discord.Interaction, onoff: bool):
    settings = getDataU(interaction.user.id)
    
    settings['dmblocker'] = bool_to_int(onoff)
    userSettings.update(interaction.user.id, settings)
    await interaction.response.send_message(f"✅ dmblocker setting updated to **{onoff}**")
    
  
  @app_commands.command(name = "ping", description="Shows connectivity information of the bot")
  async def ping(self, interaction: discord.Interaction):
    shard = self.bot.get_shard(interaction.guild.shard_id)
    color = colorSetup(interaction.user.id)
    em = discord.Embed(color=color,description = f'Pong!🏓\nPing: {round(shard.latency * 1000)}ms\nShard {shard.id} of {shard.shard_count}')
    
    await interaction.response.send_message(embed = em)

  #TODO: after all json 'db' have been rewritten
  @app_commands.command(name = "removedata", description="removes all your data from the bot")
  async def removedata(self, interaction: discord.Interaction):
    class rmdata(discord.ui.View):
      def __init__(self, interaction: discord.Interaction):
        super().__init__()
        self.value = None
        self.interaction = interaction
      @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.danger)
      async def cfm(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user.id != self.interaction.user.id:
          await interaction.response.send_message(content = "Not your menu, idiot", ephemeral=True)
          return
        self.value = True
        for child in self.children:
          child.disabled = True
        await self.interaction.edit_original_response(content = "confirmed. good riddance!", view=self)
        await interaction.response.defer()
        userSettings.delete(interaction.user.id)
        
        
      @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.primary)
      async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False
        for child in self.children:
          child.disabled = True
        await self.interaction.edit_original_response(content = "cancelled, sad.", view=self)
        await interaction.response.defer()

    view = rmdata(interaction)
    await interaction.response.send_message(content="Are you sure you wanna remove your data from the bot?\nYou will lose your personal settings.", view = view) 
    await view.wait()
    

    if view.value is None:
      for child in view.children:
        child.disabled = True
      await interaction.edit_original_response(content = "Timed out, loser", view = view)
    
    
        
    
  
    
  server_group = app_commands.Group(name="serversettings", description="Shows the settings for this server", guild_only = True)

  @server_group.command(name = "menu", description="Shows the menu for server settings")
  @app_commands.checks.has_permissions(manage_guild=True)
  async def s_menu(self, interaction: discord.Interaction):
    settings = getData(interaction.guild.id)
    blacklist_ids = [userid for userid in eval(settings.get('blacklist'))]

    blacklist = await asyncio.gather(*[interaction.client.fetch_user(uid) for uid in blacklist_ids])
    

    color = colorSetup(interaction.user.id)
    blacklist = ', '.join([usr.mention for usr in blacklist]) or None 
    em = discord.Embed(color = color)
    em.set_author(name = 'Annoybot Server Settings')
    em.add_field(name = "Autoresponse (autoresponse)",value = f"Current: **{bool(settings.get('autoresponse'))}**\nTurns /autoresponse on/off" ,inline= False)
    em.add_field(name = "Blacklist users (blacklist)", value = f"Current list: **{blacklist}**\nBlacklists certain users from using annoybot commands " ,inline= False)

    
    await interaction.response.send_message(embed =em, ephemeral=True)
    
  @server_group.command(name = "autoresponse", description="Turns /autoresponse on or off")
  @app_commands.describe(onoff = "On or off")
  @app_commands.checks.has_permissions(manage_guild=True)
  async def s_auto(self, interaction: discord.Interaction, onoff : bool):
    settings = getData(interaction.guild.id)
    
    settings['autoresponse'] = bool_to_int(onoff)
    serverSettings.update(interaction.guild.id, settings)

    
    await interaction.response.send_message(f"✅ autoresponse setting updated to **{onoff}**",ephemeral=True)
    
    
  @server_group.command(name = "blacklist", description="Blacklists certain users from using the bot")
  @app_commands.describe(modify="add/remove people from the blacklist", user = "User to blacklist/unblacklist")
  @app_commands.checks.has_permissions(manage_guild=True)
  async def s_black(self, interaction: discord.Interaction, modify: Literal['add','remove'], user:discord.Member):
    settings = getData(interaction.guild.id)
    
    blacklist= eval(settings['blacklist']) #List[discord.Member]
    if modify =="add":

      #cant ban yourself
      if user.id == interaction.user.id:
        await interaction.response.send_message(f"❌ You can't blacklist yourself, dumb.",ephemeral=True)
        return

      #cant blacklist twice
      if user.id in blacklist:
        await interaction.response.send_message(f"❌ This person is already blacklisted? Get good next time.",ephemeral=True)
        return
      
      blacklist.append(user.id)
      await interaction.response.send_message(f"✅ Added {user.display_name} to blacklist",ephemeral=True)

    elif modify == "remove":
      try:
        blacklist.remove(user.id)
        await interaction.response.send_message(f"✅ Removed {user.display_name} from blacklist",ephemeral=True)
      except ValueError:
        await interaction.response.send_message(f"❌ {user.display_name} is not currently blacklisted????",ephemeral=True)
        return
    settings['blacklist'] = f'{blacklist}'

    serverSettings.update(interaction.guild.id, settings)

    
    
      
  
async def setup(bot):
  await bot.add_cog(Setups(bot))