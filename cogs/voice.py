import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio
from discord import FFmpegPCMAudio
from other.utilities import colorSetup,getData,getDataSnipe,getDataU,postTips, changeff, addDataU


from mutagen.mp3 import MP3
import math
from typing import *

class noise_view(discord.ui.View):
  def __init__(self):
    super().__init__()
  
  @discord.ui.button(label="⬜", style=discord.ButtonStyle.red)
  async def callback(self, interaction: discord.Interaction, button: discord.ui.Button):
    try:
      await interaction.guild.voice_client.disconnect()
      button.disabled =True
      button.style = discord.ButtonStyle.grey
      
      await interaction.response.edit_message(view=self)
      await interaction.followup.send("✅ disconnected successfully, imagine being that annoyed")
      
      self.stop()
      
    except AttributeError:
      await interaction.response.send_message("❌ The bot isn't in a voice channel, idiot.", ephemeral = True)
      self.stop()
      return
    except:
      await interaction.response.send_message("❌ Yikes! something went wrong.", ephemeral = True)
      self.stop()
      return
  @staticmethod
  def disabled_button():
    view = discord.ui.View()
    view.add_item(discord.ui.Button(style = discord.ButtonStyle.grey, disabled = True,label="⬜"))
    return view
    
    
  
class noise:
  def __init__(self, interaction: discord.Interaction, path: str, seconds: int):
    self.path = path
    self.interaction = interaction
    self.seconds = seconds

  #represents a success/failure, message = message if fails
  async def response(self, status: bool, message: str= None):
    view = noise_view()
    color= colorSetup(self.interaction.user.id)

    #if successful...
    if status:
      em = discord.Embed(color = color, description = f"enjoy your {self.interaction.command.name}, loser").set_footer(text="You can force the bot to disconnect with the button below, if youre a pussy that is")
      await self.interaction.response.send_message(embed=em, view = view)

    #an error was encountered!!!! wow!!!
    else:
      em = discord.Embed(color = color, description = message)
      await self.interaction.response.send_message(embed=em)

  
  async def play(self):
    try:
      channel = self.interaction.user.voice.channel
      voice = await channel.connect()
    except AttributeError:
      await self.response(False, "❌ You are not in a VC, stupid.")
      return
    except discord.ClientException:
      await self.response(False, "❌ The bot is already playing something.")
      return
    
      
    await self.response(True)
    voice.play(FFmpegPCMAudio(self.path))
    await asyncio.sleep(self.seconds)
    await self.interaction.edit_original_response(view=noise_view.disabled_button())
    
    try:
      await self.interaction.guild.voice_client.disconnect()
      
      #if already disconnected manually
    except AttributeError:
      return

    


class Voice(commands.Cog):

  def __init__(self,bot):
    self.bot = bot 
    
  @app_commands.command(name = "earrape", description="Plays an awful sound into your VC")
  @app_commands.guild_only()
  @app_commands.describe(seconds="The number of seconds to play the earrape sound")
  async def earrape(self, interaction: discord.Interaction, seconds: Optional[app_commands.Range[int,1]] = 5):
    color= colorSetup(interaction.user.id) 
    try:
      
      channel = interaction.user.voice.channel
      voice = await channel.connect()
    except AttributeError:
      await interaction.response.send_message(embed = discord.Embed(color = color, description = "❌ You are not in a VC, stupid."))
      return
    except discord.ClientException:
      await interaction.response.send_message("❌ The bot is already playing something.")
      return
    
    
    paths = ("./voice/rickroll.mp3","./voice/fallguys.mp3","./voice/kahoot.mp3","./voice/thomas.mp3","./voice/wii.mp3", "./voice/android_earrape.mp3")
    source = paths[random.randint(0,len(paths)-1)]
    audio = MP3(source)
        
    if seconds > audio.info.length:
      seconds = int(math.floor(float(audio.info.length)))
      await interaction.response.send_message(f"(The track length is maxed at {seconds}s, so playing for that amount of time)\nNow playing a random earrape piece in your vc for {seconds}s. LOL", view = noise_view())
      return
    await interaction.response.send_message("Now playing a random earrape piece in your vc for {}s. LOL".format(seconds), view = noise_view())
        
        
          
    voice.play(FFmpegPCMAudio(source))
        
    await asyncio.sleep(seconds)
    await interaction.edit_original_response(view=noise_view.disabled_button())
    
    try:
      await interaction.guild.voice_client.disconnect()
      
    except AttributeError:
      return
    
    

  playnoise = app_commands.Group(name="playnoise", description="Plays a specific noise", guild_only=True)
    
  @playnoise.command(name="fart", description="Plays a fart noise into your VC")
  async def fart(self, interaction: discord.Interaction):
    to_play = noise(interaction, "./voice/fart.mp3", 2)
    await to_play.play()
    
  
  @playnoise.command(name="micblow", description="Plays a breathing/blowing noise into your VC")
  async def micblow(self, interaction: discord.Interaction):
    to_play = noise(interaction, "./voice/mic.mp3", 5)
    await to_play.play()

  
  @playnoise.command(name="asmr", description="Plays a chewing noise into your VC")
  async def asmr(self, interaction: discord.Interaction):
    to_play = noise(interaction, "./voice/asmr.mp3", 10)
    await to_play.play()

  
  @playnoise.command(name="cartoon", description="Plays a goofy cartoon noise into your VC")
  async def cartoon(self, interaction: discord.Interaction):
    to_play = noise(interaction, "./voice/cartoon.mp3", 20)
    await to_play.play()

  
  @playnoise.command(name="cbat", description="Plays cbat into your VC")
  async def cbat(self, interaction: discord.Interaction):
    to_play = noise(interaction, "./voice/mic.mp3", 15)
    await to_play.play()
    
  @playnoise.command(name="scream", description="Plays a female screaming noise into your VC")
  async def scream(self, interaction: discord.Interaction):
    to_play = noise(interaction, "./voice/scream.mp3", 2)
    await to_play.play()
    

  @playnoise.command(name="rickroll", description="Plays Never Gonna Give You Up (Rick Astley, 1987) into your VC")
  async def rickroll(self, interaction: discord.Interaction):
    to_play = noise(interaction, "./voice/rick_astley.mp3", 210)
    await to_play.play()

  @playnoise.command(name="indianinsult", description="Plays the voice of an indian dude insulting your cock into your VC")
  async def indian(self, interaction: discord.Interaction):
    to_play = noise(interaction, "./voice/indian_shitpost.mp3", 40)
    await to_play.play()

  @playnoise.command(name="fnafscream", description="plays the scream of freddy fazbear from fnaf")
  async def fnaf(self, interaction: discord.Interaction):
    to_play = noise(interaction, "./voice/fnaf_scream.mp3", 6)
    await to_play.play()

  @playnoise.command(name="androidearrape", description="plays a bass boosted android notification sound")
  async def android(self, interaction: discord.Interaction):
    to_play = noise(interaction, "./voice/android_earrape.mp3", 4)
    await to_play.play()
  
    
async def setup(bot):
  await bot.add_cog(Voice(bot))