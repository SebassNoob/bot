
import discord
from discord.ext import commands
from discord import app_commands
import random


class Message(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
    self.emojispam = app_commands.ContextMenu(
      name = 'spam emojis',
      callback = self.emojispam
    )
    self.uwuify = app_commands.ContextMenu(
      name = 'mAkE uWu',
      callback = self.uwuify
    )
    self.ratio = app_commands.ContextMenu(
      name = 'ratio',
      callback = self.ratio
    )
    self.bot.tree.add_command(self.emojispam)
    self.bot.tree.add_command(self.uwuify)
    self.bot.tree.add_command(self.ratio)

  @app_commands.checks.has_permissions(read_message_history=True, add_reactions=True)
  async def emojispam(self, interaction: discord.Interaction, message: discord.Message):
    await interaction.response.send_message("attempting to spam emojis...")
    emojis = [
      "😛",
      "🤭",
      "🤨",
      "🙄",
      "🤥",
      "😴",
      "🤮",
      "🐵",
      "🦍",
      "🍆",
      "🍒",
      "🍑",
      "🥰",
      "🤞",
      "🖕",
      "💀"
      "🔥"
    ]
    random.shuffle(emojis)
    try:
      for e in range(7):
      
        await message.add_reaction(emojis[e])
    except Exception as e:
      await interaction.edit_original_response(content = f"something goofed. ```{e}```")
    await interaction.edit_original_response(content = "done. loser")

    
  async def uwuify(self, interaction: discord.Interaction, message: discord.Message):
    if message.content == "":
      await interaction.response.send_message("This message is empty?", ephemeral = True)
      return
    to_mod = message.content.lower()
    out = ''.join([char.upper() if pos%2==0 else char for pos, char in enumerate(to_mod)])
    
    await interaction.response.send_message(out)
  @app_commands.checks.has_permissions(read_message_history=True, add_reactions=True)
  async def ratio(self, interaction: discord.Interaction, message: discord.Message):
    accompany = (
      "No one cares",
      "Shut the fuck up",
      "L",
      "Who asked?",
      "Your opinion is invalid",
      "No one gives 2 shits about your opinion",
      "Get good",
      "Uninstall discord mate",
      "Really? nobody asked"
    )
    em = discord.Embed(color = 0x000000, description = f" '{message.content}'")
    em.add_field(name=random.choice(accompany) + " + ratio", value = '\u200b')
    em.set_author(name=f"Replying to {message.author.name}", icon_url=message.author.display_avatar)
    await interaction.response.send_message(embed = em)
    
    await (await interaction.original_response()).add_reaction("👍")

async def setup(bot):
  await bot.add_cog(Message(bot))