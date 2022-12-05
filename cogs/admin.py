
import discord
from discord.ext import commands
import asyncio
import sys
import os


#dangerous admin-only commands
class Admin(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot

    
  @commands.command()
  @commands.is_owner()
  async def servers(self, ctx):
    for server in self.bot.guilds:
      await asyncio.sleep(0.2)
      await ctx.send(f"{server.name}: {server.id}")
  
    
  
  
  @commands.command()
  @commands.is_owner()
  async def sysexit(self, ctx):
    

    await ctx.send("Bot has been taken offline.")
    sys.exit()
  

  @commands.command()
  @commands.is_owner()
  async def restart(self, ctx):

    await ctx.send("Bot is restarting...")
    os.system("python restart.py")

    
  
  @commands.command()
  @commands.is_owner()
  async def sync(self, ctx):
    await ctx.channel.send("attempting to sync...")
    await self.bot.tree.sync()
    await ctx.channel.send("synced!")


async def setup(bot):
  await bot.add_cog(Admin(bot))