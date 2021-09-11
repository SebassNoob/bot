import discord
from discord.ext import commands
import random
import asyncio
from discord import FFmpegPCMAudio
import os
from other.customCooldown import CustomCooldown
from other.upvoteExpiration import getUserUpvoted
class Voice(commands.Cog):

  def __init__(self,bot):
    self.bot = bot 
    
  @commands.command()
  @commands.check(CustomCooldown(1, 10, 1, 5, commands.BucketType.user, elements=getUserUpvoted()))
  async def earrape(self,ctx,seconds = None):
    try:
      if seconds == None:
        seconds = 20
      channel = ctx.author.voice.channel
      voice = await channel.connect()
      paths = ("./voice/rickroll.mp3","./voice/fallguys.mp3","./voice/kahoot.mp3","./voice/thomas.mp3","./voice/wii.mp3")
      source = FFmpegPCMAudio(paths[random.randint(0,len(paths)-1)])
      await ctx.reply("Now playing a random earrape in your vc for {}s. LOL".format(seconds))
      voice.play(source)
      


      await asyncio.sleep(int(seconds))
      await ctx.guild.voice_client.disconnect()
      
      

    except AttributeError:
      await ctx.send(embed = discord.Embed(color = 0x000000, description = "You are not in a VC, stupid."))
    
      

  @commands.command(name = "disconnect",aliases = ["dc"])
  @commands.check(CustomCooldown(1, 10, 1, 5, commands.BucketType.user, elements=getUserUpvoted()))
  async def disconnect(self,ctx):
    await ctx.guild.voice_client.disconnect()
    await ctx.reply("✔️ confirmed")
    

def setup(bot):
    bot.add_cog(Voice(bot))