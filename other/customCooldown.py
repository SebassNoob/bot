import discord
import os
from discord.ext import commands
from discord import app_commands
#TODO: implement upvote check
def CustomCooldown(interaction: discord.Interaction):
  
  if interaction.user.id == os.environ['uid']:
    return None
  if 858200514914287646 in [a.id for a in interaction.user.mutual_guilds]:
    #12 commands per 30 seconds, triggers a 30 sec cooldown
    return app_commands.Cooldown(12,30)
  #10 commands per 30 seconds, triggers a 30 sec cooldown
  return app_commands.Cooldown(10,30)
  