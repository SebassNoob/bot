import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord import app_commands
import os
import sys
from other.asyncCmds import colorSetup,getData,getDataSnipe,getDataU,postTips, changeff, addDataU
import random
import json
import base64
import aiohttp
import io

import requests
from waifu import WaifuClient
from typing import *


from pyinsults import insults
import other.serverSettings as serverSettings
import asyncio
import csv
sys.path.insert(1,'./other')
from sqliteDB import create_db, get_db_connection




class anime_embed(discord.Embed):
  def __init__(self, pic_type: str, interaction_user: discord.Interaction.user, image_url: str):
      
    self.pic_type = pic_type
    super().__init__(color=colorSetup(interaction_user.id))
    self.set_author(name = f"{pic_type} requested by {interaction_user.display_name}",icon_url = interaction_user.display_avatar).set_image(url=image_url)
  def define(self):
    desc = {
      "waifu" : "A fictional female character from  an anime, manga, or video game to whom one is romantically attracted",
      "neko": "A woman with cat ears, whiskers, and sometimes paws or a tail.",
      "shinobu": "A fictional character with this surname",
      "megumin": "A fictional character with this surname" ,
      "bully": "A woman who bullies others into submission",
      "cuddle": "A person who is cuddling something",
      "cry": "An anime character crying",
      "hug": "An anime character hugging something",
      "kiss": "An anime character kissing something",
      "lick": "An anime character licking something",
      "blush": "An anime character blushing",
      "smile": "An anime character smiling",
      "wave": "An anime character waving", 
      "happy": "An anime character being happy",
      "dance": "An anime character dancing"
      
    }
    return desc[self.pic_type]                                                        
      
class nerd(discord.ui.View):
  def __init__(self, em: anime_embed):
    super().__init__()
    self.em = em

  @discord.ui.button(label="🤓 Hopefully apt description", style=discord.ButtonStyle.grey)
  async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
    await interaction.response.send_message(self.em.define(), ephemeral=True)
        


class Misc(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
  

  utils = app_commands.Group(name="utils", description="Random utilities that fit the rude theme.")

  
  @utils.command(name="pick", description="Picks a random option from a list of given words.")
  @app_commands.describe(arguments="The hex code of the color you want in your embeds.")
  async def pick(self,interaction: discord.Interaction, arguments: str):
    addDataU(interaction.user.id)
    choice = random.choice([arg.strip() for arg in arguments.split(',')])
    
    insult = changeff(insults.random_insult()) if bool(getDataU(interaction.user.id).get("familyFriendly")) else insults.random_insult()
    
    await interaction.response.send_message(f'{interaction.user.mention}\nI pick {choice}, you indecisive {insult}.')
        



  
  @utils.command(name = "8ball", description="Gives you a yes/no answer based on a given question")
  @app_commands.describe(question="The yes/no question you want to ask")
  async def predict(self, interaction: discord.Interaction, question: str):
    addDataU(interaction.user.id)
    predictions = ["hmm yes i think so.","nah mate sry.","You DARE ask me this question?! Well i'm not going to give ya an answer",'not too sure about this one. try again.','Your short answer: NO',"answer's no, gtfo of here scrub.","omg YES","Are you actually stupid? Its NO.","Are you actually stupid? Its YES moron.","you gotta be kidding right, its yes.", "this question is too difficult even for my huge brain. However, at least I have one.","no.",'yes, stupid.',"you're rather stupid aren't you, answer is yes.", "You moronic bastard, its kinda obious isn't it?! NO!"]
        
    prediction = changeff(random.choice(predictions)) if bool(getDataU(interaction.user.id).get("familyFriendly")) else random.choice(predictions)
      

       
    color = colorSetup(interaction.user.id)
    em = discord.Embed(color = color)
      
    em.add_field(name = question, value = prediction,inline = False)
    em.set_footer(text=f"requested by {interaction.user.display_name}")
    
    await interaction.response.send_message(embed=em)

  
  autoresponse = app_commands.Group(name="autoresponse", description="The bot will respond to a list of predetermined words", guild_only=True)

  def autoresponse_ui_handler(self, interaction: discord.Interaction, key_values) -> Tuple[discord.Embed, Optional[discord.File]]:
  
    desc = "ID/Keyword: Response\n"
    desc +=''.join([f'\n{i} {row[0]}: {row[1]}' for i, row in enumerate(key_values)])
    
    
    f = discord.File(io.StringIO(desc), 'table') if len(desc)>4000 else None
      
        
    color = colorSetup(interaction.user.id)
    em = discord.Embed(color = color,description = f"``{desc if len(desc) <= 4000 else 'The autoresponse table is too large. The table will be sent as an attachment'}``")
    em.set_author(name = "Autoresponse keywords")
    em.set_footer(text="Mods can turn this off in /serversettings and edit with /autoresponse add or /autoresponse remove")
    return em, f
    


  @autoresponse.command(name = "menu", description= "A list of words the bot will respond to in your server.")
  async def auto_menu(self, interaction: discord.Interaction):
    
    key_values = eval(serverSettings.get(interaction.guild_id)['autoresponse_content']).items()
    
    em, f = self.autoresponse_ui_handler(interaction, key_values)
    if not f:
      await interaction.response.send_message(embed=em)
      return
    await interaction.response.send_message(embed=em, file = f)
    

  @autoresponse.command(name="add", description="Add autoresponse keywords")
  @app_commands.checks.has_permissions(manage_guild=True)
  @app_commands.describe(word="The word you want the bot to respond to", response="The resulting response to the aforementioned word")
  async def add(self, interaction: discord.Interaction, word: app_commands.Range[str, 1, 1500], response: app_commands.Range[str, 1, 1500]):
    
    to_update = serverSettings.get(interaction.guild_id)
    key_values = eval(to_update['autoresponse_content'])

    
    key_values.update({word: response})
    
    to_update['autoresponse_content']= f'{key_values}'
    
    
    serverSettings.update(interaction.guild_id, to_update)


    key_values = key_values.items() #ensures consistency
    em, f = self.autoresponse_ui_handler(interaction, key_values)
    if not f:
      await interaction.response.send_message(content = f"✅ Added ``{word} : {response}``. Here is the new list.",embed=em)
      return
    await interaction.response.send_message(content = f"✅ Added ``{word} : {response}``. Here is the new list.",embed=em, file=f)
    
    
  @autoresponse.command(name="remove", description="Remove autoresponse keywords")
  @app_commands.checks.has_permissions(manage_guild=True)
  @app_commands.describe(id="The numeric id of the word response pair you want to remove. You can check this id at  /autoresponse menu")
  async def remove(self, interaction: discord.Interaction, id: int):
    
    to_update = serverSettings.get(interaction.guild_id)

    #a list of tuples with autoresponse k-v pairs
    key_values = list(eval(to_update['autoresponse_content']).items())
    try:
      removed = key_values.pop(id)
    except IndexError:
      await interaction.response.send_message(content="❌ Enter a proper id, idiot. Use /autoresponse menu to check the id.", ephemeral = True)
      return

      
    res = {k:v for k,v in key_values}
    

    
    to_update['autoresponse_content']= f'{res}'
    serverSettings.update(interaction.guild_id, to_update)
    
    
    em, f = self.autoresponse_ui_handler(interaction, key_values)
    if not f:
      await interaction.response.send_message(content = f"✅ Removed ``{removed[0]} : {removed[1]}``. Here is the new list.",embed=em)
      return
    await interaction.response.send_message(content = f"✅ Removed ``{removed[0]} : {removed[1]}``. Here is the new list.",embed=em, file = f)
    
  @autoresponse.command(name="resetdb", description="Reset the autoresponse menu to it's default state.")
  @app_commands.checks.has_permissions(manage_guild=True)
  async def resetdb(self, interaction: discord.Interaction):

    #confirmation
    color = colorSetup(interaction.user.id)
    em = discord.Embed(color = color, description="Are you certain you want to reset this server's autoresponse settings?")
    
    class Confirm(discord.ui.View):
      def __init__(self, interaction: discord.Interaction):
        super().__init__()
        self.value = None
        self.interaction = interaction

    
      @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
      async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.interaction.user.id:
        
          await interaction.response.send_message('Not your button, dumbass', ephemeral=True)
          return
        await interaction.response.send_message('Confirming', ephemeral=True)

        
        self.value = True
        
        self.stop()

    
      @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
      async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.interaction.user.id:
          await interaction.response.send_message('Not your button, dumbass', ephemeral=True)
          return
        await interaction.response.send_message('Cancelling', ephemeral=True)
        self.value = False
        self.stop()


    
    view = Confirm(interaction)
    await interaction.response.send_message(embed = em, view = view )


    await view.wait()
    original = await interaction.original_response()
    if not view.value:
      await original.edit(view = discord.ui.View()
                          .add_item(item = discord.ui.Button(style = discord.ButtonStyle.success, label = "Confirm", disabled = True))
                          .add_item(item = discord.ui.Button(style = discord.ButtonStyle.grey, label = "Cancel", disabled = True))
                          )
      return

      
    


    
    with open("./json/autoresponse.csv",newline="") as file:
      reader = list(csv.DictReader(file))
      #getting default
      autores = {i['word']: i['response'] for i in reader}

      
    to_update = serverSettings.get(interaction.guild_id)
    

    #resetting the db
    to_update['autoresponse_content'] = f'{autores}'
    
    
    serverSettings.update(interaction.guild.id, to_update)

    #UI
    desc = "ID/Keyword: Response\n"
    desc +=''.join([f'\n{i} {row[0]}: {row[1]}' for i, row in enumerate(list(autores.items()))])
    
    
    em = discord.Embed(color = color,description = f"``{desc}``")
    em.set_author(name = "Autoresponse keywords")
    em.set_footer(text="Mods can turn this off in /serversettings and edit with /autoresponse add or /autoresponse remove")
    
    await original.edit(content = f"✅ Resetted database to default. Here is the new list.",embed=em, view = None)
     
    
  
  
  @app_commands.command(name="meme", description="Sends a top meme from reddit")
  async def meme(self, interaction: discord.Interaction):


    subreddits = ['https://www.reddit.com/r/dankmemes/new.json?sort=hot','https://www.reddit.com/r/okbuddyretard/new.json?sort=hot','https://www.reddit.com/r/memes/new.json?sort=hot',
    'https://www.reddit.com/r/wholesomememes/new.json?sort=hot', 'https://www.reddit.com/r/meme/new.json?sort=hot', 'https://www.reddit.com/r/PrequelMemes/new.json?sort=hot','https://www.reddit.com/r/deepfriedmemes/new.json?sort=hot', 'https://www.reddit.com/r/nukedmemes/new.json?sort=hot']
    async with aiohttp.ClientSession() as cs:

      async with cs.get(subreddits[random.randint(0,len(subreddits)-1)]) as r:
        res = await r.json()
        
        color = colorSetup(interaction.user.id)
        
        
        try:
          randomn = random.randint(0,15)
          embed = discord.Embed(color = color,title = res['data']['children'] [randomn]["data"]["title"])
        
          embed.set_image(url=res['data']['children'] [randomn]['data']['url'])
          

        except KeyError as e:
          await interaction.response.send_message("❌ An unknown error occured, try again.")
          raise e
            
        

    await interaction.response.send_message(embed=embed)


  @app_commands.command(name="snipe", description="Sends the most recently deleted messaage of a user.")
  @app_commands.guild_only()
  @app_commands.describe(user="The user you want to snipe")
  async def snipe(self,interaction: discord.Interaction, user: discord.Member):
    addDataU(user.id)
    if not bool(getDataU(user.id)['sniped']):
      await interaction.response.send_message("❌ This guy can't be sniped, what a loser. (/settings sniped off)")
      return
    #implement nsfw check
    

    

    try:
      message, time, nsfw = getDataSnipe(user.id)
    #if function returns none 
    except TypeError:
      await interaction.response.send_message("There's nothing to snipe!")
      return
    
    if bool(getDataU(user.id)['familyFriendly']):
      message = changeff(message)

    
    if nsfw:
      if isinstance(interaction.channel, (discord.abc.GuildChannel,discord.Thread)) and not interaction.channel.nsfw:
        await interaction.response.send_message("The user you mentioned last deleted their message in a nsfw channel. 🔞")
        return
      
    
    
    color = colorSetup(interaction.user.id)
      
    embed = discord.Embed(color= color,description=message)        
    embed.set_footer(text=f"UTC {time}")
        
    embed.set_author(name= f"Quote from {user.name}", icon_url = user.display_avatar)
    
    await interaction.response.send_message(embed=embed)

  

  

  @app_commands.command(name="anime", description="Sends a pic of an anime woman")
  @app_commands.describe(type="Type of picture you want to see")
  async def anime(self, interaction: discord.Interaction, type: Literal['waifu', 'neko','shinobu', "megumin","bully","cuddle", "cry", "hug","kiss","lick","blush","smile","wave","happy","dance"]):
    pic = WaifuClient().sfw(category=type)
    em = anime_embed(type,interaction.user, pic)
    
    
    await interaction.response.send_message(embed = em, view = nerd(em))
    
  
    
  
  @app_commands.command(name = "iplookup", description="Finds the location of a given ip")
  @app_commands.describe(ip="The ip you want to find the location of")
  async def iplookup(self, interaction: discord.Interaction,ip: str):
    color = colorSetup(interaction.user.id)
    url = f"http://ip-api.com/json/{ip}"
    res = requests.get(url).json()
    
    
    
    if res['status'] != "success":
          
      await interaction.response.send_message("❌ Thats not a valid ip, idiot.", ephemeral=True)
      return
          
          
    try:
      country = res["country"] or "Unknown" 
      region = res["regionName"] or "Unknown" 
      city = res["city"] or "Unknown"  
      zip_code= res["zip"] or "Unknown" 
      latitude = res['lat'] or "Unknown"  
      longitude = res['lon'] or "Unknown" 
      provider = res['isp'] or "Unknown" 
    except KeyError:
      await interaction.response.send_message("❌ An unspecified error occured, the ip address probably is private. What a loser lmao.")
      return
    await interaction.response.send_message(embed =discord.Embed(color = color, title = ip,description = f"**country**:{country}\n**region**:{region}\n**city**:{city}\n**zip code**:{zip_code}\n**coordinates**: ({latitude},{longitude})\n**ISP**:{provider}"))
      

  @app_commands.command(name="textwall", description="Sends a wall of repeated text in a single message")
  @app_commands.describe(num = "The number of times to spam", content="What to spam")
  async def textwall(self, interaction: discord.Interaction, num:int, content: str):
    
    toSend = ''
    for i in range(num):
      toSend += f'{content.strip()} '
    if len(toSend) > 2000:
      await interaction.response.send_message("❌ Your text wall is too long (>2000 characters), you moron.")
      return
    if bool(getDataU(interaction.user.id)['familyFriendly']):
      toSend = changeff(toSend)
    await interaction.response.send_message(toSend)

  @app_commands.command(name="urbandict", description="Looks up a term in urban dictionary")
  @app_commands.describe(term = "The term you want to search")
  async def urbandict(self, interaction: discord.Interaction, term: str):
    
  
    url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
    
    querystring = {"term":term}
    
    headers = {
        'x-rapidapi-key': "eb9abc1708msh9ff61d9af0e2802p1a89dejsncd366a92c2b6",
        'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com"
        }
    
    response = requests.request("GET", url, headers=headers, params=querystring)
    color = colorSetup(interaction.user.id)
    try:
      em = discord.Embed(color = color, title=f"Urban Dictionary result for {term}", description = "Definition: "+response.json()['list'][0]["definition"]+"\n\nExamples: "+response.json()['list'][0]["example"])
      await interaction.response.send_message(embed = em)
    except IndexError:
      await interaction.response.send_message("❌ there were no results returned, actually search for a real word next time, you moron.")
    
  
async def setup(bot):
  await bot.add_cog(Misc(bot))

