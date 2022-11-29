import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import os 
from other.asyncCmds import colorSetup ,addDataU,getDataU, postTips
from discord import app_commands
from typing import List
import json
import asyncio
import re
from typing import *
import other.userSettings as userSettings
from other.customCooldown import CustomCooldown
from other.upvoteExpiration import getUserUpvoted
import datetime

class Setups(commands.Cog):
  
  def __init__(self, bot):
        self.bot = bot

    
  @commands.command()
  @commands.is_owner()
  async def sync(self, ctx) -> None:
      
    await self.bot.tree.sync()
    await ctx.send("Synced!")
    
  @app_commands.command(name = "info", description="Shows general information and support links.")
  async def credit(self, interaction: discord.Interaction):
    view = discord.ui.View() 
    guilds = len(self.bot.guilds)
    username = await self.bot.fetch_user(int(os.environ['uid']))
    color = colorSetup(interaction.user.id)
    embedVar3 = discord.Embed(color = color)
    embedVar3.add_field(name = "Annoybot 1.8.0", value = "Developed by " +str(username)+"\nLibrary: discord.py 2.1.0\n[dbl link](https://discordbotlist.com/bots/annoybot-4074)\n[AYB link](https://ayblisting.com/bots/844757192313536522)\nServer count: "+ str(guilds),inline = False)

    buttons = [
      discord.ui.Button(
        style=discord.ButtonStyle.link, 
        label="top.gg", 
        url="https://top.gg/bot/844757192313536522"
      ),
      discord.ui.Button(
        style=discord.ButtonStyle.link, 
        label="invite", 
        url="https://discord.com/api/oauth2/authorize?client_id=844757192313536522&permissions=1490084293971&scope=bot%20applications.commands"
      ),
      discord.ui.Button(
        style=discord.ButtonStyle.link, 
        label="support server", 
        url="https://discord.gg/UCGAuRXmBD"
      ),
    
    ] 
    for button in buttons:
      view.add_item(item=button)
    
    await interaction.response.send_message(embed = embedVar3, view=view)




  
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
      embedVar3.add_field(name = "``pick (list)``", value = "Randomly chooses from a list of arguments the user provides.",inline = False)
      embedVar3.add_field(name = "``predict (question)``", value = "Predicts the answer to a yes/no question.",inline = False)
      embedVar3.add_field(name = "``autoresponse``", value = "Responds to certain keywords guild-wide and sends a message in return. \nRequires user to have **manage_server** permission.",inline = False)
      embedVar3.add_field(name = "``textwall(num,content)``", value = "Sends a wall of text up to 2000 characters.",inline = False)
      embedVar3.add_field(name = "``meme``", value = "Sends a meme.",inline = False)
      embedVar3.add_field(name = "``snipe (user)``", value = "Shows a user's recently deleted message.",inline = False)
      embedVar3.add_field(name = "``anime (type)``", value = "Shows a picture of an anime girl.",inline = False)
      embedVar3.add_field(name = "``iplookup(ip)``", value = "Looks up somebody's ip LOL.",inline = False)
      embedVar3.add_field(name = "``urbandict(text)``", value = "looks for the definition of the given word on urban dictionary.",inline = False)
      
  
      embedVar4 = discord.Embed(color = color)
      embedVar4.set_author(name="Annoybot commands (trolls)\nAll troll commands have a 10s cooldown.")
      
      embedVar4.add_field(name = "``channeltroll (user)``", value = "Creates a private new channel and pings the trolled user 3 times. When either the trolled user speaks in the channel or 2 minutes have passed, the channel is deleted.\nRequires bot to have **manage_channels** permission.",inline = False)
      embedVar4.add_field(name = "``nicktroll (user,*threat)``", value = "Changes the nickname of a user temporarily to either a random set of characters or a chosen nickname.\nRequires bot to have **manage_nicknames** permission.",inline = False)
      embedVar4.add_field(name = "``dmtroll (user)``", value = "Ping the affected user 3 times in their dms, then deletes it.",inline = False)
  
      embedVar4.add_field(name = "``ghosttroll (user)``", value = "Ghost pings the user in 3 different channels.",inline = False)
      
  
      embedVar4.add_field(name = "``fakeban (user)``", value = "Fakes a ban for the trolled user. WARNING: USER WILL BE KICKED. Requires bot to have **create_instant_invite** and **kick_members** permissions and user needs **kick_members** permission. ",inline = False)
  
      embedVar4.add_field(name = "``fakemute (user,*reason)``", value = "Fakes a mute for the trolled user. If no reason is given, a random one will be generated. ",inline = False)
      embedVar4.add_field(name = "``nitrotroll``",value = "Fakes a nitro gift in chat. Clicking on claim will produce a rickroll. Requires **manage_messages** permissions.")
      
      embedVar5 = discord.Embed(color = color)
      embedVar5.set_author(name="Annoybot commands (games)\nAll games commands have a 10s cooldown.")
      embedVar5.add_field(name = "``memorygame``", value = "Memorise the pattern shown at the start of the level and try to replicate it from memory afterward.",inline = False)
      embedVar5.add_field(name = "``tictactoe (user)``", value = "Play tictactoe with a friend!",inline = False)
      embedVar5.add_field(name = "``vocabularygame``",value = "Test your vocabulary skills with this game! Requires bot to have **add_reaction** permission.", inline = False)
      embedVar5.add_field(name = "``typingrace``",value = "Race with others and see who can type the fastest!", inline = False)
      embedVar5.add_field(name = "``wouldyourather``",value = "Challenge your friends to a would you rather game. Best experienced in a VC!", inline = False)
      embedVar5.add_field(name = "``truthordare``", value = "Play a game of truth or dare with your friends. Best played in a VC or physically!", inline = False)
      
      embedVar6 = discord.Embed(color = color)
      embedVar6.set_author(name="Annoybot commands (setup)")
      embedVar6.add_field(name = "``daily``", value = "Gives you 30mins of reduced cooldowns once per day!",inline = False)
      embedVar6.add_field(name = "``patchnotes``", value = "Shows the latest patch notes!",inline = False)
      embedVar6.add_field(name = "``settings (*option, *value)``", value = "Shows user settings. ",inline = False)
      embedVar6.add_field(name = "``info``", value = "Sends links to support this bot!",inline = False)
      embedVar6.add_field(name = "``resetdata``", value = "Resets and removes all your data from the bot.", inline = False)
      embedVar6.add_field(name = "``legal``", value = "Shows legal stuff. eh.", inline = False)
  
      embedVar7 = discord.Embed(color = color)
      embedVar7.set_author(name="Annoybot commands (voice)\nAll voice commands have a 10s cooldown.")
      embedVar7.add_field(name = "``earrape (*duration)``", value = "Joins your VC and plays a random earrape song",inline = False)
      embedVar7.add_field(name = "``fart``", value = "Joins your VC and plays a fart sfx",inline = False)
      embedVar7.add_field(name = "``micblow``", value = "Joins your VC and simulates blowing into a mic",inline = False)
      embedVar7.add_field(name = "``scream``", value = "Joins your VC and screams into it.",inline = False)
      embedVar7.add_field(name = "``rickroll``", value = "plays the legendary rick astley song and force everyone to listen.",inline = False)
      embedVar7.add_field(name = "``disconnect``", value = "Disconnects the bot from the VC.",inline = False)
      return [embedVar,embedVar3,embedVar4,embedVar5,embedVar6,embedVar7]


    
    class options(discord.ui.Select):
      def __init__(self):
        options = [
          discord.SelectOption(label="Core features", description = "A list of features considered to be the main highlights.", emoji="🌌"),
          discord.SelectOption(label="Setup", description = "Commands to aid in configuration of the bot", emoji = "⚙️"),
          discord.SelectOption(label="Troll", description="Commands to troll your friends", emoji ="👺"),
          discord.SelectOption(label= "Voice", description="Commands used in voice channels to be annoying", emoji="🎤"),
          discord.SelectOption(label="Games", description="Games you can play with friends", emoji ="🎲"),
          discord.SelectOption(label="Misc", description="Contains some random features.", emoji="🌎")
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
          "Misc": pages[1]
          
        }
        
        await interaction.response.edit_message(embed= get_page.get(value), view = view)
        
    

    


    
    
    
    view = discord.ui.View()
    view.add_item(item=options())
    await interaction.response.send_message(content = "The values in brackets are additional arguments you're supposed to give. * denotes an optional argument.", embed = contents()[0], view = view )

    #legacy code
    '''
    instruct = await ctx.send(embed = discord.Embed(color = color, description = "The values in brackets are additional arguments you're supposed to give. * denotes an optional argument."))
    mainMessage = await ctx.send(
        
        embed = paginationList[current],
        components = [ 
          Select(placeholder="Other pages", options=[SelectOption(label="Main features", value="0"), SelectOption(label="Misc", value="1"), SelectOption(label="Trolls", value="2"), SelectOption(label="Games", value="3"), SelectOption(label="Setup", value="4"), SelectOption(label="Voice", value="5")])]
        
    )
    
    while True:
        
        try:
            
            
            interaction = await self.bot.wait_for(
                "select_option", 
                check = lambda i: True,
                timeout = 60.0 
            )
            
            

            current = int(interaction.values[0])
            await interaction.respond(
                type = 7,
                embed = paginationList[current],
              
            )
        except asyncio.TimeoutError:
          await mainMessage.delete()
          await instruct.delete()
          break
'''



  settings_group = app_commands.Group(name="settings", description="Shows your settings for the bot")
  
  
  @settings_group.command(name = "menu", description="Shows what your settings are")
  async def settings(self,interaction: discord.Interaction):
    
    settings = getDataU(interaction.user.id)
    
    color = colorSetup(interaction.user.id)
      
    em = discord.Embed(color = color)
    em.set_author(name = 'Annoybot User Settings')
    em.add_field(name = "Preferred embed colour (color)",value = f"Current: **{settings.get('color')}**\nChanges the colour of embed sent through the bot to a specific colour." ,inline= False)
    em.add_field(name = "Family Friendly (familyfriendly)", value = f"Current: **{bool(settings.get('familyFriendly'))}**\nCensors some swear words. " ,inline= False)
    em.add_field(name = "Can be sniped (sniped)", value = f"Current: **{bool(settings.get('sniped'))}**\nDetermines if you can be sniped by others." ,inline= False)
    em.add_field(name = "Can be dm'ed (dmblocker)", value = f"Current: **{bool(settings.get('dmblocker'))}**\nDetermines if you can be dm'ed by the bot." ,inline= False)
    
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
  async def ff(self, interaction: discord.Interaction, onoff: Literal['on', 'off']):
    settings = getDataU(interaction.user.id)
    
    settings['familyFriendly'] = 1 if onoff =='on' else 0
    userSettings.update(interaction.user.id, settings)
    await interaction.response.send_message(f"✅ familyfriendly setting updated to **{onoff}**", ephemeral=True)

  @settings_group.command(name = "sniped", description="Allows your messages to be stored to be sniped by /snipe")
  async def sniped(self, interaction: discord.Interaction, onoff: Literal['on', 'off']):
    settings = getDataU(interaction.user.id)
    
    settings['sniped'] = 1 if onoff =='on' else 0
    userSettings.update(interaction.user.id, settings)
    await interaction.response.send_message(f"✅ sniped setting updated to **{onoff}**")
    
  @settings_group.command(name = "dmblocker", description="Blocks the bot from sending private messages to you.")
  async def dmblocker(self, interaction: discord.Interaction, onoff: Literal['on', 'off']):
    settings = getDataU(interaction.user.id)
    
    settings['dmblocker'] = 1 if onoff =='on' else 0
    userSettings.update(interaction.user.id, settings)
    await interaction.response.send_message(f"✅ dmblocker setting updated to **{onoff}**")
    
  
  @app_commands.command(name = "ping", description="Shows connectivity information of the bot")
  async def ping(self, interaction: discord.Interaction):
    shard = self.bot.get_shard(interaction.guild.shard_id)
    color = colorSetup(interaction.user.id)
    em = discord.Embed(color=color,description = f'Pong!🏓\nPing: {round(shard.latency * 1000)}ms\nShard {shard.id} of {shard.shard_count}')
    
    await interaction.response.send_message(embed = em)

  #TODO: after all json 'db' have been rewritten
  @commands.command()
  async def removedata(self,ctx):
    await ctx.send("This command will ERASE ALL YOUR DATA. Type ``yes`` or ``no`` to continue.")
    try:
      msg = await self.bot.wait_for("message",check = lambda i: i.author.id==ctx.author.id,timeout = 30)
      if msg.content.lower() == "yes":
        uid = ctx.author.id
        with open("./json/userSnipeCache.json","r") as f:
          snipe = json.load(f)
          
        with open("./json/userSettings.json","r") as f:
          settings = json.load(f)
          
        with open("./json/upvoteData.json","r") as f:
          upvote = json.load(f)
          
        with open("./json/egg.json","r") as f:
          egg = json.load(f)
          
        toDelete =[snipe,settings,upvote,egg]
        for i in range(4):
          try:
            del toDelete[i][str(uid)]
          except:
            pass
        with open("./json/userSnipeCache.json","w") as f:
          json.dump(snipe,f)
        with open("./json/userSettings.json","w") as f:
          json.dump(settings,f)
        with open("./json/upvoteData.json","w") as f:
         json.dump(upvote,f)
        with open("./json/egg.json","w") as f:
         json.dump(egg,f)
         
        await ctx.send("Thanks for freeing up my drive space, good riddance.")
      elif msg.content.lower() =="no":
        await ctx.send("ok, I won't be erasing your data today.")
        
      else:
        await ctx.send("ok, I won't be erasing your data today.")
    except asyncio.TimeoutError:
      await ctx.send("ok, I won't be erasing your data today.")
    
  @app_commands.command(name="legal", description="Shows the licence, privacy policy and TOS.")
  async def legal(self, interaction: discord.Interaction):
    view = discord.ui.View() 

    components = [ 
      discord.ui.Button(
        label = "licence",
        url = "https://pastebin.com/7rGBHDCU",
        style = discord.ButtonStyle.link
                      
      ),
      discord.ui.Button(
        label = "privacy policy",
        url = "https://pastebin.com/fS86u0Hw",
        style = discord.ButtonStyle.link
                      
      ),
      discord.ui.Button(
        label = "terms of service",
        url = "https://pastebin.com/43VFzdJx",
        style = discord.ButtonStyle.link
                      
                      
      ),
      discord.ui.Button(
        label = "README.md",
        url = "https://pastebin.com/e7jLvVHr",
        style = discord.ButtonStyle.link
                      
                      
      )
    ]
    for button in components:
      view.add_item(button)
    await interaction.response.send_message(content="Here are our legal documents, nerd.", view=view)
    
      
      
  
async def setup(bot):
  await bot.add_cog(Setups(bot))