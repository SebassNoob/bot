import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio
from discord import FFmpegPCMAudio

from other.customCooldown import CustomCooldown
from other.upvoteExpiration import getUserUpvoted
from mutagen.mp3 import MP3
import math
from typing import *

class noise:
  def __init__(self, interaction: discord.Interaction, path: str, seconds: int):
    self.path = path
    self.interaction = interaction
    self.seconds = seconds
  
  async def play(self):
    try:
      channel = self.interaction.user.voice.channel
      voice = await channel.connect()
    except AttributeError:
      await self.interaction.response.send_message(embed = discord.Embed(color = 0x000000, description = "❌ You are not in a VC, stupid."))
      return
    await self.interaction.response.send_message(embed = discord.Embed(color = 0x000000, description = f"✅ enjoy your {self.interaction.command.name}, loser").set_footer(text="You can force the bot to disconnect with /disconnect, if youre a pussy that is"))
    voice.play(FFmpegPCMAudio(self.path))
    await asyncio.sleep(self.seconds)
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
  async def earrape(self, interaction: discord.Interaction, seconds: Optional[int] = 5):
    try:
      
      channel = interaction.user.voice.channel
      voice = await channel.connect()
    except AttributeError:
      await interaction.response.send_message(embed = discord.Embed(color = 0x000000, description = "❌ You are not in a VC, stupid."))
      return
    
    
    paths = ("./voice/rickroll.mp3","./voice/fallguys.mp3","./voice/kahoot.mp3","./voice/thomas.mp3","./voice/wii.mp3")
    source = paths[random.randint(0,len(paths)-1)]
    audio = MP3(source)
        
    if seconds > audio.info.length:
      seconds = int(math.floor(float(audio.info.length)))
      await interaction.response.send_message(f"(The track length is maxed at {seconds}s, so playing for that amount of time)\nNow playing a random earrape in your vc for {seconds}s. LOL")
    await interaction.response.send_message("Now playing a random earrape in your vc for {}s. LOL".format(seconds))
        
        
          
    voice.play(FFmpegPCMAudio(source))
        
    await asyncio.sleep(seconds)
    try:
      await interaction.guild.voice_client.disconnect()
    except AttributeError:
      return
    
      

  @app_commands.command(name = "disconnect", description="Disconnects the bot from any vc in the server")
  async def disconnect(self, interaction: discord.Interaction):
    try:
      await interaction.guild.voice_client.disconnect()
      await interaction.response.send_message("✅ disconnected successfully, imagine being that annoyed")
      
    except AttributeError:
      await interaction.response.send_message("❌ The bot isn't in a voice channel, stupid.", ephemeral = True)
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

    
  @playnoise.command(name="scream", description="Plays a female screaming noise into your VC")
  async def scream(self, interaction: discord.Interaction):
    to_play = noise(interaction, "./voice/scream.mp3", 2)
    await to_play.play()
    

  @playnoise.command(name="rickroll", description="Plays Never Gonna Give You Up (Rick Astley, 1987) into your VC")
  async def rickroll(self, interaction: discord.Interaction):
    to_play = noise(interaction, "./voice/rick_astley.mp3", 210)
    await to_play.play()
    
async def setup(bot):
  await bot.add_cog(Voice(bot))