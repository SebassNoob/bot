import discord
from discord.ext import commands
import random
import asyncio
from discord import FFmpegPCMAudio
import os
from other.customCooldown import CustomCooldown
from other.upvoteExpiration import getUserUpvoted
from mutagen.mp3 import MP3
import math
class Voice(commands.Cog):

  def __init__(self,bot):
    self.bot = bot 
    
  @commands.command()
  @commands.check(CustomCooldown(1, 10, 1, 5, commands.BucketType.user, elements=getUserUpvoted()))
  async def earrape(self,ctx,seconds: int = 20):
    try:
      
      channel = ctx.author.voice.channel
      voice = await channel.connect()

      

    except AttributeError:
      await ctx.send(embed = discord.Embed(color = 0x000000, description = "You are not in a VC, stupid."))
      raise Exception
    
    try:
        paths = ("./voice/rickroll.mp3","./voice/fallguys.mp3","./voice/kahoot.mp3","./voice/thomas.mp3","./voice/wii.mp3")
        source = paths[random.randint(0,len(paths)-1)]
        audio = MP3(source)
        
        if seconds > audio.info.length:
          seconds = int(math.ceil(float(audio.info.length)))
          await ctx.send(f"(The track length is maxed at {seconds}s)")
        await ctx.reply("Now playing a random earrape in your vc for {}s. LOL".format(seconds))
        
        
        
          
        voice.play(FFmpegPCMAudio(source))
        
        await asyncio.sleep(seconds)
        await ctx.guild.voice_client.disconnect()
    except: 
        pass
      

  @commands.command(name = "disconnect",aliases = ["dc"])
  @commands.check(CustomCooldown(1, 10, 1, 5, commands.BucketType.user, elements=getUserUpvoted()))
  async def disconnect(self,ctx):
    try:
      await ctx.guild.voice_client.disconnect()
      await ctx.reply("✔️ confirmed")
      
    except AttributeError:
      await ctx.reply("The bot isn't in a voice channel, stupid.")
      raise Exception
    
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
def setup(bot):
    bot.add_cog(Voice(bot))