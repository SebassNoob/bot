import discord
import os

from discord import app_commands
import sqlite3
import datetime

#TODO: implement upvote check
async def CustomCooldown(interaction: discord.Interaction):
  if interaction.user.id == int(os.environ['uid']):

    return None
  guild = interaction.client.get_guild(858200514914287646) 
  
  if guild and guild.get_member(interaction.user.id): 

    return app_commands.Cooldown(12,30)

  
  return app_commands.Cooldown(8,30)
  