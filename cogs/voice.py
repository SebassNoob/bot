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
      await interaction.response.send_message("✔️ disconnected successfully, imagine being that annoyed")
      
    except AttributeError:
      await interaction.response.send_message("❌ The bot isn't in a voice channel, stupid.", ephemeral = True)
      return
    
  @commands.command()
  @commands.check(CustomCooldown(1, 10, 1, 5, commands.BucketType.user, elements=getUserUpvoted()))
  async def fart(self,ctx):
    try:
      
      channel = ctx.author.voice.channel
      voice = await channel.connect()

      

    except AttributeError:
      await ctx.send(embed = discord.Embed(color = 0x000000, description = "You are not in a VC, stupid."))
      raise Exception
    try:
      
      seconds = 2
      await ctx.reply("Farting in ur vc...")
      voice.play(FFmpegPCMAudio("./voice/fart.mp3"))
      await asyncio.sleep(seconds)
      await ctx.guild.voice_client.disconnect()
    except: 
      pass

  
  @commands.command()
  @commands.check(CustomCooldown(1, 10, 1, 5, commands.BucketType.user, elements=getUserUpvoted()))
  async def micblow(self,ctx):
    try:
      
      channel = ctx.author.voice.channel
      voice = await channel.connect()

      

    except AttributeError:
      await ctx.send(embed = discord.Embed(color = 0x000000, description = "You are not in a VC, stupid."))
      raise Exception
    try:
      
      seconds = 5
      await ctx.reply("Blowing a mic into ur vc")
      voice.play(FFmpegPCMAudio("./voice/mic.mp3"))
      await asyncio.sleep(seconds)
      await ctx.guild.voice_client.disconnect()
    except: 
      pass

  @commands.command()
  @commands.check(CustomCooldown(1, 10, 1, 5, commands.BucketType.user, elements=getUserUpvoted()))
  async def scream(self,ctx):
    try:
      
      channel = ctx.author.voice.channel
      voice = await channel.connect()

      

    except AttributeError:
      await ctx.send(embed = discord.Embed(color = 0x000000, description = "You are not in a VC, stupid."))
      raise Exception
    try:
      
      seconds = 2
      await ctx.reply("Screaming into your vc")
      voice.play(FFmpegPCMAudio("./voice/mic.mp3"))
      await asyncio.sleep(seconds)
      await ctx.guild.voice_client.disconnect()
    except: 
      pass


  @commands.command()
  @commands.check(CustomCooldown(1, 10, 1, 5, commands.BucketType.user, elements=getUserUpvoted()))
  async def rickroll(self,ctx):
    try:
      
      channel = ctx.author.voice.channel
      voice = await channel.connect()

      

    except AttributeError:
      await ctx.send(embed = discord.Embed(color = 0x000000, description = "You are not in a VC, stupid."))
      raise Exception
    try:
      seconds=float(MP3("./voice/rick_astley.mp3").info.length)
      voice.play(FFmpegPCMAudio("./voice/rick_astley.mp3"))
      await asyncio.sleep(seconds)
      await ctx.guild.voice_client.disconnect()
    except: 
      pass
async def setup(bot):
  await bot.add_cog(Voice(bot))