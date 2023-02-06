import discord
from discord.ext import commands
from discord import app_commands
from difflib import SequenceMatcher
from typing import *
import json
import asyncio
import random
import string
from other.asyncCmds import colorSetup


import threading
import time
import datetime
import math
from pyinsults import insults
import csv




# Defines a custom button that contains the logic of the game.
# The ['TicTacToe'] bit is for type hinting purposes to tell your IDE or linter
# what the type of `self.view` is. It is not required.
class TicTacToeButton(discord.ui.Button['TicTacToe']):
    def __init__(self, x: int, y: int):
        # A label is required, but we don't need one so a zero-width space is used
        # The row parameter tells the View which row to place the button under.
        # A View can only contain up to 5 rows -- each row can only have 5 buttons.
        # Since a Tic Tac Toe grid is 3x3 that means we have 3 rows and 3 columns.
        super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y

    # This function is called whenever this particular button is pressed
    # This is part of the "meat" of the game logic
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.user1:
            if interaction.user.id != view.user1.id:
              await interaction.response.send_message(content = "It's not your turn, stupid", ephemeral = True)
              return
            self.style = discord.ButtonStyle.danger
            self.label = 'X'
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.user2
            content = f"It is now {view.user2.mention}'s' turn"
        else:
            if interaction.user.id != view.user2.id:
              await interaction.response.send_message(content = "It's not your turn, stupid", ephemeral = True)
              return
            self.style = discord.ButtonStyle.success
            self.label = 'O'
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.user1
            content = f"It is now {view.user1.mention}'s turn"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = f'{view.user1.mention} won!'
            elif winner == view.O:
                content = f'{view.user2.mention} won!'
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


# This is our actual board View
class TicTacToe(discord.ui.View):
    # This tells the IDE or linter that all our children will be TicTacToeButtons
    # This is not required
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self, user1: discord.User, user2: discord.User):

        super().__init__()
        self.current_player = user1
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        self.user1 = user1
        self.user2 = user2
        

        # Our board is made up of 3 by 3 TicTacToeButtons
        # The TicTacToeButton maintains the callbacks and helps steer
        # the actual game.
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

        
    
    
    # This method checks for the board winner -- it is used by the TicTacToeButton
    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        # If we're here, we need to check if a tie was made
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None


class MemButton(discord.ui.Button['Mem']):
    def __init__(self, x: int, y: int):

        super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y

    # This function is called whenever this particular button is pressed
    # This is part of the "meat" of the game logic
    async def callback(self, interaction: discord.Interaction):
      
        
        assert self.view is not None
        view: MemGame = self.view
        if interaction.user.id != view.interaction.user.id:
          await interaction.response.send_message("Not your game!", ephemeral = True)
        for child in view.children:
          child.label = '\u200b'
          child.style = discord.ButtonStyle.secondary
        if view.check(self.x, self.y): #if check is true (passed)
          

          #edit the button properties
          self.style=discord.ButtonStyle.success
          self.label = "✓" #TODO: replace witha unicode tick
          
        else:
          self.style = discord.ButtonStyle.danger
          self.label = "✗" #TODO: replace with unicode cross
          for child in view.children:
            child.disabled = True
          view.stop()
          expectedTime = ((view.level*(view.level+1))/2)*(3.5+view.level)
    
          bonus = expectedTime/((datetime.datetime.now() - view.time).total_seconds())
          if bonus <1:
            bonus = 1
          score = view.level*bonus
          color = colorSetup(view.interaction.user.id)
          em = discord.Embed(color=color)
          em.add_field(name="stats",value=f"Level: {view.level}\nTime bonus: \u00D7{round(bonus,2)}\n**Score: {math.ceil(score)}**",inline = False)
          await interaction.channel.send(embed = em)
        await interaction.response.edit_message(content = f"Memory Game: Level {view.level}\nReplicate the sequence of highlighted squares to the best of your memory.", view=view)
        if view.pattern == []:
          await view.levelup()


# This is our actual board View
class MemGame(discord.ui.View):

    children: List[MemButton]


    def __init__(self, interaction: discord.Interaction):

        super().__init__()

        self.level = 1
        self.pattern = [] #list[tuple[x,y]]
        self.interaction = interaction
        self.time = datetime.datetime.now()
        
        for x in range(3):
            for y in range(3):
                self.add_item(MemButton(x, y))
    async def async_init(self):
      self.original_res = await self.interaction.original_response()
    def generate_pattern(self):
      coords = [(a.x, a.y) for a in self.children] # a list of coords eg. (0,1) corresponding to each button pressed 
      self.pattern.append(random.choice(coords))
      return 
    async def instructions(self):
      #edit the view (level) times displaying the color as green 
      for child in self.children:
        child.label = '\u200b'
        child.disabled = True


       
      await self.original_res.edit(content = f"Memory Game: Level {self.level}\nReplicate the sequence of highlighted squares to the best of your memory.", view = self)
      
      
      for i, coord in enumerate(self.pattern, start = 1):
        x, y = coord
        #set properties of the child
        for child in self.children:

          child.style = discord.ButtonStyle.secondary
          child.label = '\u200b'

        def get_child(child):
          if child.x == x and child.y == y:
            return True
          return False
          #unsure
        
        child = list(filter(get_child, self.children))[0]

        child.style = discord.ButtonStyle.success
        child.label = i
        await self.original_res.edit(view = self)
        await asyncio.sleep(1)
        
      for child in self.children:
        child.disabled = False
        child.style = discord.ButtonStyle.secondary
        child.label = '\u200b'
        
      await self.original_res.edit(view = self)
        
      return 
    def check(self, x: int, y: int) -> bool:
      #check if x,y is first in pattern
      if (x,y) == self.pattern[0]:
        self.pattern.remove((x,y))
        
        return True
      return False
    async def levelup(self):
      self.level += 1
      for _ in range(self.level):
        self.generate_pattern()
      await self.instructions()
      
    async def start(self):
      self.generate_pattern()
      await self.instructions()

    


class Games(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(name = "memorygame", description = "Sets up a game to test your visual memory")
  async def memorygame(self, interaction: discord.Interaction):
    view = MemGame(interaction)
    
    await interaction.response.send_message(content = f"Memory Game: Level {view.level}\nReplicate the sequence of highlighted squares to the best of your memory.", view = view)
    await view.async_init()
    await view.start()
    

    
  @app_commands.command(name = "tictactoe", description="Starts a game of tictactoe with another user")
  @app_commands.describe(user = "The user you want to challenge")
  async def tictactoe(self, interaction: discord.Interaction , user: discord.User):
    if user.id == interaction.user.id:
      await interaction.response.send_message(content = "You can't challange yourself, silly", ephemeral = True)
      return
    if user.bot:
      await interaction.response.send_message(content = "You can't challenge a bot, duh?", ephemeral = True)
      return
    await interaction.response.send_message(content = f"TicTacToe: {interaction.user.mention} goes first", view = TicTacToe(interaction.user, user))

        

  @app_commands.command(name = "vocabularygame", description = "Test your vocabulary with this game")
  @app_commands.checks.bot_has_permissions(add_reactions = True)
  async def vocabularygame(self,interaction: discord.Interaction):
    
    

    await interaction.response.defer(thinking=True)
    file = open("./json/words.txt","r")
    words = [w.lower().replace('\n','') for w in file.readlines()]
    

    vowels = ["a","e","i","o","u"]
    randomLetters = ''.join(random.choices(string.ascii_lowercase,k=9))
    for i in range(3):
      randomLetters = randomLetters + vowels[random.randint(0,4)]
      
    await interaction.followup.send(f"With the letters ``{randomLetters}`` type as many words as you can within 30s!")
    
    reqLetters= list(randomLetters)
    
    def check(str,set):
      
      try:
        for c in list(str):
          
          set.remove(c)
          set.append(c)
      except ValueError:
        
        return False
      return True
    
      
    

    
    def timer(t): 
      while t !=0:
        time.sleep(1)
        t -=1
      return
    thr = threading.Thread(target = timer, args = (30,))
    thr.start()
    score = 0                             
    combo = 0
    maxcombo = 0
    accuracy = 0
    correct = 0
    used_words = []
    bonus = 0
    
    while thr.is_alive():
      
      
      
      try:

        msg = await self.bot.wait_for(
        "message",
        check = lambda i: i.author.id == interaction.user.id and i.channel.id == interaction.channel.id, 
        timeout = 1
      )
        

        
        if msg.content in words and msg.content not in used_words and check(msg.content,reqLetters):
          await msg.add_reaction("✅")
          used_words.append(msg.content)
          correct +=1
          score += 100
          combo += 1
          if maxcombo < combo:
            maxcombo+=1
          
          score+= combo*25
        elif not check(msg.content,reqLetters) or msg.content not in words:
          used_words.append(msg.content)
          combo = 0
        
        
      except asyncio.TimeoutError:
        continue
    try:
      accuracy = correct/len(used_words)
    except ZeroDivisionError:
      accuracy = 0
      
    bonus = score*(accuracy/8)
    score += bonus
        
    
      
      
    color = colorSetup(interaction.user.id)
    em = discord.Embed(color=color)
    em.add_field(name = "``Stats``",value=f"Accuracy: {math.ceil(accuracy*100)}%\nNumber of correct words: {correct}\nMax combo: {maxcombo}\nAccuracy bonus: +{math.ceil(bonus)}\n**Total score: {math.ceil(score)}**",inline=False)
    await interaction.channel.send(embed = em)
    
    
        
    
    
  
  @app_commands.command(name = "typingrace", description = "Race against others to see who can type the quickest")
  @app_commands.checks.bot_has_permissions(add_reactions = True)
  async def typingrace(self, interaction: discord.Interaction):
    
    class join_race(discord.ui.View):
      def __init__(self):
        super().__init__()
        self.joined = [] #List[discord.Member]
        with open('./json/typingrace.txt', 'r') as f:
          self.text = random.choice([l.replace('\n','') for l in f.readlines()])
          self.anticheat_text = '\u200b'.join([char for char in self.text])
      def disable_buttons(self):
        for b in self.children:
          b.disabled=True

        return self
      @discord.ui.button(label="Join race!", style = discord.ButtonStyle.blurple)
      async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user in self.joined:
          await interaction.response.send_message(f"You've already joined, {insults.long_insult()}", ephemeral = True)
          return
        self.joined.append(interaction.user)
        await interaction.response.send_message("You've joined the race successfully.", ephemeral = True)
      @discord.ui.button(label="Start race!", style = discord.ButtonStyle.blurple)
      async def start(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        await interaction.response.edit_message(view = self.disable_buttons())
        await interaction.channel.send(embed = discord.Embed(color = colorSetup(interaction.user.id)).add_field(name="Typing race starts now! Type the following within 180s:", value= f"``{self.anticheat_text}``", inline = False).set_footer(text=f"Participating users: {', '.join([str(u.display_name) for u in self.joined])}"))
    race_buttons = join_race()
    await interaction.response.send_message(content="Join the typing race here!", view = race_buttons)
    st_time = datetime.datetime.now()
    #race_buttons.text for text
    
    def timer(t): 
      while t !=0:
        time.sleep(1)
        t -=1
      return
    thr = threading.Thread(target = timer, args = (180,))
    thr.start()
    accuracy = 0
    wpm = 0 
    penalty = 0
    
    leaderboards = {}
    def check_accuracy(input, text):
      return SequenceMatcher(None, input, text).ratio()
      
    while thr.is_alive():
      try:
        msg = await self.bot.wait_for("message", check = lambda i: i.author in race_buttons.joined and i.channel.id == interaction.channel.id,timeout = 1)
        time_taken = (datetime.datetime.now() - st_time).total_seconds()
        await msg.add_reaction("✅")

        #calc score
        accuracy = round(check_accuracy(msg.content, race_buttons.text), 3) #round to 3sf
        if accuracy < 0: accuracy = 0
        race_buttons.joined.remove(msg.author)
        wpm = math.ceil(len(msg.content.split(" "))/(time_taken/60))

        penalty = math.floor(wpm*(1-accuracy))
        wpm -= penalty

        leaderboards[msg.author.id] = {
          "accuracy": accuracy,
          "penalty": penalty,
          "wpm": wpm
        }
        
        
      except asyncio.TimeoutError:
        continue

    def arr_in_order(lb: List[Tuple[int, Dict[str, int]]]):

      arranged_lb = []

      for item in lb:
        
        if arranged_lb == list():

          arranged_lb.append(item)

          continue

        for i, wpm in enumerate(arranged_lb):
          
          if item[1]['wpm'] <= wpm[1]['wpm']:
            
            arranged_lb.insert(i,item)
            break
          elif item[1]['wpm'] > wpm[1]['wpm']:
            arranged_lb.append(item)
            break
            
          
            

      return arranged_lb[::-1]

    disp = arr_in_order(leaderboards.items())

    em = discord.Embed(color = 0xffffff, description = "**Leaderboard**")
    for place, player in enumerate(disp, start = 1):

      user = await self.bot.fetch_user(player[0])

      em.add_field(name =f"{place}/ {user.display_name}", value = f"Accuracy: {player[1]['accuracy']*100}%\nPenalty:{player[1]['penalty']} wpm\nTotal:{player[1]['wpm']} wpm", inline= False)
    
    await interaction.channel.send(embed = em)
      
      



  @app_commands.command(name = "wouldyourather", description="Generates a would you rather question")
  async def wouldyourather(self, interaction: discord.Interaction):
    with open('./json/wyr_options.json', 'r') as f:
      options_list = list(json.load(f).items())
      options_tuple = random.choice(options_list)
    
      #tuple[str,str]
    class options(discord.ui.View):
      def __init__(self):
        super().__init__()
        self.who = {
          "op1": [],
          "op2": []
        }
        self.voted = []
      @discord.ui.button(label="Option 1", style=discord.ButtonStyle.green)
      async def op1(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id in self.voted:
          await interaction.response.send_message(f"You've already voted, you {insults.long_insult()}. ", ephemeral=True)
          return
        await interaction.response.send_message("You voted for option 1!", ephemeral=True)
        
        self.who['op1'].append(interaction.user.display_name)
        self.voted.append(interaction.user.id)
        
      @discord.ui.button(label="Option 2", style=discord.ButtonStyle.green)
      async def op2(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id in self.voted:
          await interaction.response.send_message(f"You've already voted, you {insults.long_insult()}. ", ephemeral = True)
          return
        await interaction.response.send_message("You voted for option 2!", ephemeral=True)
        self.who['op2'].append(interaction.user.display_name)
        self.voted.append(interaction.user.id)

      def results(self):
        return (self.who, self.voted)
        
    
    
    color = colorSetup(interaction.user.id)
    em = discord.Embed(color = color)
    em.add_field(name = "Would you rather...", value = f"1. {options_tuple[0]}\n2. {options_tuple[1]} ",inline = False)
    em.set_footer(text = "Best played in a voice call!")
    view= options()
    await interaction.response.send_message("You have 30s to select one of the below!",embed = em, view = view)
    
        
    await asyncio.sleep(10)  
    
    
    
    results, voted= view.results()
    for b in view.children:
      b.disabled = True
    interaction_msg = await interaction.original_response()
    await interaction.followup.edit_message(interaction_msg.id, view=view)
    class review_results(discord.ui.View):
      def __init__(self, results, em_color):
        super().__init__()
        self.results = results
        self.color = em_color
      @discord.ui.button(label = "See who voted for what", style=discord.ButtonStyle.blurple)
      async def clback(self, interaction: discord.Interaction, button: discord.ui.Button):
        em = discord.Embed(color = self.color, description=f"Option 1: {', '.join(self.results['op1'])}\nOption 2: {', '.join(self.results['op2'])}")
        await interaction.response.send_message(embed = em, ephemeral =True)
    em2 = discord.Embed(color = color)
    try:
      em2.add_field(name = "Results!", value = f"``{(len(results['op1'])/len(voted))*100}%`` {options_tuple[0]}\n``{(len(results['op2'])/len(voted))*100}%`` {options_tuple[1]}",inline = False)
    except ZeroDivisionError:
      em2.add_field(name = "Results!", value = f"``0%`` {options_tuple[0]}\n``0%`` {options_tuple[1]}",inline = False)
    em2.set_footer(text = "Best played in a voice call!")
    await interaction.channel.send(embed = em2, view = review_results(results, color))
      


  @app_commands.command(name="truthordare", description="Generates a truth or dare question")
  async def truthordare(self, interaction: discord.Interaction):
    color = colorSetup(interaction.user.id)
    with open("./json/TorD.csv",newline="") as file:
      arr = list(csv.DictReader(file))
      #looks like List[Dict[str, Union[int, str]]]

    class tord(discord.ui.View):
      def __init__(self):
        super().__init__()
      def reroll(self):
        class reroll(discord.ui.View):
          def __init__(self, func):
            super().__init__()
            self.func = func
          @discord.ui.button(label="reroll", style=discord.ButtonStyle.grey)
          async def re(self, interaction: discord.Interaction, button: discord.ui.Button):

            await self.func.callback(interaction)
        
        return reroll

        
      @discord.ui.button(label="Truth", style=discord.ButtonStyle.green)
      async def op1(self, interaction: discord.Interaction, button: discord.ui.Button):
        #type == 0 means truth

        choices = list(filter(lambda i: i['type'] == "0",arr))
        truth = random.choice(choices)['content']
        
        await interaction.response.edit_message(content = truth, view = self.reroll()(self.op1))
        
        
        
      @discord.ui.button(label="Dare", style=discord.ButtonStyle.green)
      async def op2(self, interaction: discord.Interaction, button: discord.ui.Button):

        choices = list(filter(lambda i: i['type'] == "1",arr))
        dare = random.choice(choices)['content']
        
        await interaction.response.edit_message(content=dare, view = self.reroll()(self.op2))
        

        
    await interaction.response.send_message("Truth or dare?", view =tord() )

        

            
        

    


  


async def setup(bot):
  await bot.add_cog(Games(bot))