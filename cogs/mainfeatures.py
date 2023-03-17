import discord
from discord import app_commands
from discord.ext import commands

import csv
from other.utilities import colorSetup,changeff,getDataU,addDataU,postTips

import random

from typing import *
import requests


from dadjokes import Dadjoke
from pyinsults import insults


class MainFeatures(commands.Cog):
  
  def __init__(self, bot):
        self.bot = bot


  @app_commands.command(name = "roast", description = "Roasts someone.")
  @app_commands.describe(user="The person you wanna roast")
  async def roast(self,interaction: discord.Interaction ,user: Optional[Union[discord.Member, discord.User]] = None):
    if user: addDataU(user.id)
    addDataU(interaction.user.id)
    with open('./json/roast.txt', 'r') as f:
      roast = random.choice([r.replace('\n','') for r in f.readlines()])
        
    if bool(getDataU(interaction.user.id).get("familyFriendly")):
      roast = changeff(roast)
    color = colorSetup(interaction.user.id)
    embedVar = discord.Embed( color=color,description = roast)
    embedVar.set_author(name=f"Roast from {interaction.user.display_name}", icon_url = interaction.user.display_avatar)
          
        
    embedVar.set_footer(text="u suck")
    
    await interaction.response.send_message(content = user.mention if user else '', embed = embedVar)


  
  
  @app_commands.command(name = "insult", description="Generates an insult and targets someone.")
  @app_commands.describe(user="Someone to insult")
  async def insult(self, interaction: discord.Interaction, user: Optional[Union[discord.Member, discord.User]] = None):
    if user: addDataU(user.id)
    addDataU(interaction.user.id)
    sentence_starter=[
      "You",
      "Go fuck yourself, you",
      "Shut up,",
      "Fuck off,",
      "Have a great day, you",
      "You're such a"
      
    ]
    insult= f"{random.choice(sentence_starter)} {random.choice([insults.long_insult(), insults.random_insult()])}!"

    if bool(getDataU(interaction.user.id).get("familyFriendly")):
      insult = changeff(insult)

        
    
    color = colorSetup(interaction.user.id)
    embed = discord.Embed(color =color,description = insult)
        
    embed.set_footer(text="requested by " +'{}'.format(interaction.user.display_name))
    

    await interaction.response.send_message(content= user.mention if user else '', embed= embed)
      

        


  
  @app_commands.command(name = 'urmom' , description="Generates a 'yo mom' joke")
  async def urmom(self,interaction: discord.Interaction):
    with open('./json/urmom.txt', 'r') as f:
      joke = random.choice([r.replace('\n','') for r in f.readlines()])
        
    if bool(getDataU(interaction.user.id).get("familyFriendly")):
      joke = changeff(joke)
    color = colorSetup(interaction.user.id)
    
  
    embed = discord.Embed(color = color, description = joke)
    embed.set_footer(text="requested by " +'{}'.format(interaction.user.display_name)+"\nimagine having a mom.")

        
    await interaction.response.send_message(embed=embed)


 
  @app_commands.command(name = "uninspire", description="Generates an uninspirational quote.")
  async def uninspire(self, interaction: discord.Interaction):
    with open('./json/uninspire.txt', 'r') as f:
      quote = random.choice([r.replace('\n','') for r in f.readlines()])
        
    if bool(getDataU(interaction.user.id).get("familyFriendly")):
      quote = changeff(quote)
    color = colorSetup(interaction.user.id)


    embed = discord.Embed(color = color, description = quote)
    embed.set_footer(text="requested by " +'{}'.format(interaction.user.display_name))
    
    await interaction.response.send_message(embed=embed)
  
  
  @app_commands.command(name="dmthreaten", description= "Sends a threat to a direct message channel of a user. ")
  @app_commands.rename(customThreat="customthreat")
  @app_commands.describe(user = "User to threaten", customThreat="A custom message")
  async def dmthreaten(self, interaction: discord.Interaction, user: Union[discord.Member, discord.User], customThreat: Optional[app_commands.Range[str,1, None]] = None):
    addDataU(user.id)
    addDataU(interaction.user.id)
    with open('./json/dmthreaten.txt', 'r') as f:
      
      threat = random.choice([r.replace('\n','') for r in f.readlines()])
        
    if bool(getDataU(user.id).get("familyFriendly")):
      threat = changeff(threat)
      
    if bool(getDataU(user.id).get("dmblocker")) or user.bot:
      await interaction.response.send_message(content="❌ The user you mentioned is either a bot, or does not want to be DM'ed. Bet you look stupid now.", ephemeral=True)
      return 

    channel = await user.create_dm()
    color = colorSetup(interaction.user.id)

    em = discord.Embed(color = color,description = customThreat or threat)
    em.set_author(name = f"{interaction.user.display_name} from {interaction.guild.name}" if interaction.guild else interaction.user.display_name ,icon_url = interaction.user.avatar)

    try:
      await channel.send(embed = em)
    except:
      await interaction.response.send_message(f"❌ {user.display_name} blocked my message, what a pussy")
      return
    await interaction.response.send_message(content = f"✅ {user.display_name} has been sent this in DMs:", embed = em)
    
    


  @app_commands.command(name="dadjoke", description="Sends a typical dad joke.")
  async def dadjoke(self, interaction: discord.Interaction):
    
    
    dadJoke = Dadjoke().joke
    color = colorSetup(interaction.user.id)
    em = discord.Embed(color = color, description= dadJoke)
    em.set_author(name = f"{interaction.user.display_name}'s dad joke", icon_url = interaction.user.avatar)
    
    await interaction.response.send_message(embed = em)
  
  
  @app_commands.command(name="dumbdeath", description="Makes up a fictional scenario where the person you mentioned died a dumb death")
  @app_commands.describe(user="Someone who will suffer the dumb death")
  async def dumbdeath(self,interaction: discord.Interaction, user: Union[discord.Member, discord.User]):
    addDataU(user.id)
    addDataU(interaction.user.id)
    color = colorSetup(interaction.user.id)
    
    if isinstance(interaction.channel, discord.abc.GuildChannel):
      nsfw = interaction.channel.nsfw 
    elif isinstance(interaction.channel, discord.Thread):
      nsfw = interaction.channel.parent.nsfw
    else:
      nsfw = True
    
    
    with open("./json/dumbdeath.csv",newline="") as file:
      reader = list(csv.DictReader(file))
      
      
      # if nsfw anything is ok
      # else filter
      
      if not nsfw:
        reader = list(filter(lambda item: item['nsfw']=='0', reader))
        
      choice = random.choices(reader)
      
    em = discord.Embed(color = color, description = choice[0]['content'].replace("#", user.name).replace(";",","))
    await interaction.response.send_message(content=user.mention, embed = em)
            
  '''
    def choose():
      if ctx.channel.nsfw == False:
        while True:
          ran = arr[random.randint(0, len(arr)-1)]
          if ran["nsfw"] == "1":
            continue
          elif ran["nsfw"] == "0":
            return ran["content"]
      elif ctx.channel.nsfw== True:
      
        return arr[random.randint(0, len(arr)-1)]["content"]
    
    em = discord.Embed(color = color, description =choose().replace("#", user.name).replace(";",","))
    await ctx.send("{}".format(user.mention))
    await ctx.send(embed =em)
  '''

  @app_commands.command(name="darkjoke", description="Sends a dark joke. May be insensitive.")
  async def darkjoke(self, interaction: discord.Interaction):
    addDataU(interaction.user.id)
    with open('./json/darkjoke.txt', 'r') as f:
      
      joke = random.choice([r.replace('\n','') for r in f.readlines()])
        
    if bool(getDataU(interaction.user.id).get("familyFriendly")):
      joke = changeff(joke)
    
    color = colorSetup(interaction.user.id)
    await interaction.response.send_message(embed=discord.Embed(color=color,description = joke))

    
  
    
async def setup(bot):
  await bot.add_cog(MainFeatures(bot))