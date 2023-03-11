
import discord
from discord.ext import commands
import asyncio
import sys
import os
import io


#dangerous admin-only commands
class Admin(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot

    
  @commands.command()
  @commands.is_owner()
  async def servers(self, ctx):
    servers = ''.join([f"{s.name}: {s.id}\n" for s in self.bot.guilds])
    
    f = discord.File(io.StringIO(servers), 'servers.txt')
    
    await ctx.send("file created", file = f)
  
    
  
  
  @commands.command()
  @commands.is_owner()
  async def sysexit(self, ctx):
    

    await ctx.send("Bot has been taken offline.")
    sys.exit()
  

  @commands.command()
  @commands.is_owner()
  async def restart(self, ctx):

    await ctx.send("Bot is restarting...")
    os.execv(sys.argv[0])
    
    
  
  @commands.command()
  @commands.is_owner()
  async def sync(self, ctx):
    await ctx.channel.send("attempting to sync...")
    await self.bot.tree.sync()
    await ctx.channel.send("synced!")


async def setup(bot):
  await bot.add_cog(Admin(bot))