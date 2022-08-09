import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle
import asyncio
import random
import json
import string
from other.asyncCmds import colorSetup
from other.customCooldown import CustomCooldown
from other.upvoteExpiration import getUserUpvoted
import threading

import time
import math
from pyinsults import insults
import csv

class Games(commands.Cog):
  
  def __init__(self, bot):
        self.bot = bot

  @commands.command()
  @commands.check(CustomCooldown(1, 10, 1, 5, commands.BucketType.user, elements=getUserUpvoted()))
  async def memorygame(self,ctx):
    
    failed = 0
    level = 1
    color = int(await colorSetup(ctx.message.author.id),16)
    em = discord.Embed(color = color)
    em.add_field(name="Instructions:",value = "Memorise the pattern shown at the start of the level and try to replicate it from memory afterward.",inline = False)


    a= await ctx.send(embed=em)
    possibilities = ["a1", "a2","a3","b1","b2","b3","c1","c2","c3"]
    

    while failed != 1:
      cur_list = []
      for i in range(level):
        cur_list.append(possibilities[random.randint(0,8)])

      instruct = await ctx.reply(f"Memory game: Level {level}",components = [ 
              [
                  Button(
                      label = "\u200b",
                      id = "a1",
                      style = ButtonStyle.grey,
                      disabled = True
                      
                  ),
                  Button(
                      label = "\u200b",
                      id = "a2",
                      style = ButtonStyle.grey,
                      disabled = True
                      
                  ),
                  Button(
                      label = "\u200b",
                      id = "a3",
                      style = ButtonStyle.grey,
                      disabled = True
                      
                  )
              ],
              [
                Button(
                      label = "\u200b",
                      id = "b1",
                      style = ButtonStyle.grey,
                      disabled = True
                      
                  ),
                  Button(
                      label = "\u200b",
                      id = "b2",
                      style = ButtonStyle.grey,
                      disabled = True
                      
                  ),
                  Button(
                      label = "\u200b",
                      id = "b3",
                      style = ButtonStyle.grey,
                      disabled = True
                  )
              ],
              [
                Button(
                      label = "\u200b",
                      id = "c1",
                      style = ButtonStyle.grey,
                      disabled = True
                      
                  ),
                  Button(
                      label = "\u200b",
                      id = "c2",
                      style = ButtonStyle.grey,
                      disabled = True
                      
                  ),
                  Button(
                      label = "\u200b",
                      id = "c3",
                      style = ButtonStyle.grey,
                      disabled = True
                  )
              ]
          ]

      )
      for i in range(len(cur_list)):
        styles = {}
        for id in ["a1", "a2","a3","b1","b2","b3","c1","c2","c3"]:
          styles[id] = ButtonStyle.grey

        styles[cur_list[i]] = ButtonStyle.green

        labels = {}
        for id in ["a1", "a2","a3","b1","b2","b3","c1","c2","c3"]:
          labels[id] = "\u200b"

        labels[cur_list[i]] = str(i+1)

        await instruct.edit(
                    type = 7,
                    
                    components = [ 
                [
                    Button(
                        label = labels["a1"],
                        id = "a1",
                        style = styles["a1"],
                        disabled = True
                        
                    ),
                    Button(
                        label = labels["a2"],
                        id = "a2",
                        style = styles["a2"],
                        disabled = True
                        
                    ),
                    Button(
                        label = labels["a3"],
                        id = "a3",
                        style =styles["a3"],
                        disabled = True
                        
                    )
                ],
                [
                  Button(
                        label = labels["b1"],
                        id = "b1",
                        style = styles["b1"],
                        disabled = True
                        
                    ),
                    Button(
                        label = labels["b2"],
                        id = "b2",
                        style = styles["b2"],
                        disabled = True
                        
                    ),
                    Button(
                        label = labels["b3"],
                        id = "b3",
                        style = styles["b3"],
                        disabled = True
                    )
                ],
                [
                  Button(
                        label = labels["c1"],
                        id = "c1",
                        style = styles["c1"],
                        disabled = True
                        
                    ),
                    Button(
                        label = labels["c2"],
                        id = "c2",
                        style = styles["c2"],
                        disabled = True
                        
                    ),
                    Button(
                        label = labels["c3"],
                        id = "c3",
                        style = styles["c3"],
                        disabled = True
                    )
                ]
            ])
        await asyncio.sleep(1)



      await instruct.delete()


      #test below
      
      def success(arg):
        
        if arg in cur_list[0]:
          
          return True
        else:
          return False

      mainMessage = await ctx.reply(f"Memory game: Level {level}",
        components = [ 
              [
                  Button(
                      label = "\u200b",
                      id = "a1",
                      style = ButtonStyle.grey,
                      
                  ),
                  Button(
                      label = "\u200b",
                      id = "a2",
                      style = ButtonStyle.grey,
                      
                  ),
                  Button(
                      label = "\u200b",
                      id = "a3",
                      style = ButtonStyle.grey,
                      
                  )
              ],
              [
                Button(
                      label = "\u200b",
                      id = "b1",
                      style = ButtonStyle.grey,
                      
                  ),
                  Button(
                      label = "\u200b",
                      id = "b2",
                      style = ButtonStyle.grey,
                      
                  ),
                  Button(
                      label = "\u200b",
                      id = "b3",
                      style = ButtonStyle.grey,
                  )
              ],
              [
                Button(
                      label = "\u200b",
                      id = "c1",
                      style = ButtonStyle.grey,
                      
                  ),
                  Button(
                      label = "\u200b",
                      id = "c2",
                      style = ButtonStyle.grey,
                      
                  ),
                  Button(
                      label = "\u200b",
                      id = "c3",
                      style = ButtonStyle.grey,
                  )
              ]
          ]

      )
          

      def backgroundMem():
        global timerMem
        timerMem = 0
        while True:
          time.sleep(1)
          timerMem += 1
        


      score = 0
      
      threading.Thread(name='backgroundMem', target=backgroundMem).start()
      
      
      
      while True:
        try:
              interaction = await self.bot.wait_for(
                  "button_click",
                  check = lambda i: i.component.id in ["a1", "a2","a3","b1","b2","b3","c1","c2","c3"] and i.channel.id == ctx.channel.id, 
                  timeout = 30.0 
              )

              if interaction.user.id != ctx.author.id:
                await interaction.respond(type=4, content="This isn't your game, idiot.", ephemeral=True)
              else:
                labels = {}
                for id in ["a1", "a2","a3","b1","b2","b3","c1","c2","c3"]:
                  labels[id] = "\u200b"

                
                
                styles = {}
                for id in ["a1", "a2","a3","b1","b2","b3","c1","c2","c3"]:
                  styles[id] = ButtonStyle.grey

                
                if success(interaction.component.id) == True:
                  styles[interaction.component.id] = ButtonStyle.green
                  labels[interaction.component.id] = "✓"
                  try:
                    cur_list.pop(0)
                  except:
                    pass

                  
                  
                elif success(interaction.component.id) == False:
                  styles[interaction.component.id] = ButtonStyle.red
                  labels[interaction.component.id] = "✗"
                  failed = 1
                  
                
                await interaction.respond(
                      type = 7,
                      
                      components = [ 
                  [
                      Button(
                          label = labels["a1"],
                          id = "a1",
                          style = styles["a1"],
                          
                      ),
                      Button(
                          label = labels["a2"],
                          id = "a2",
                          style = styles["a2"],
                          
                      ),
                      Button(
                          label = labels["a3"],
                          id = "a3",
                          style =styles["a3"],
                          
                      )
                  ],
                  [
                    Button(
                          label = labels["b1"],
                          id = "b1",
                          style = styles["b1"],
                          
                      ),
                      Button(
                          label = labels["b2"],
                          id = "b2",
                          style = styles["b2"],
                          
                      ),
                      Button(
                          label = labels["b3"],
                          id = "b3",
                          style = styles["b3"],
                      )
                  ],
                  [
                    Button(
                          label = labels["c1"],
                          id = "c1",
                          style = styles["c1"],
                          
                      ),
                      Button(
                          label = labels["c2"],
                          id = "c2",
                          style = styles["c2"],
                          
                      ),
                      Button(
                          label = labels["c3"],
                          id = "c3",
                          style = styles["c3"],
                      )]])
              

        except asyncio.TimeoutError:
          await ctx.send("You ran out of time.")
          await a.delete()
          await mainMessage.delete()


        
        
        if len(cur_list) == 0:
          level+=1
          await mainMessage.delete()
          break
        elif failed == 1:
          timer = 0
          await asyncio.sleep(1)
          timer = timerMem
          break

    expectedTime = ((level*level+1)/2)*(5+level)
    
    bonus = expectedTime/timer
    if bonus <1:
      bonus = 1
    score = level*bonus
    await mainMessage.delete()
    await a.delete()
    color = int(await colorSetup(ctx.message.author.id),16)
    em = discord.Embed(color=color)
    em.add_field(name="stats",value=f"Level: {level}\nTime bonus: \u00D7{round(bonus,2)}\n**Score: {math.ceil(score)}**",inline = False)
    await ctx.send(embed = em)
    
  @commands.command(name = "tictactoe",aliases = ["ttt"])
  @commands.check(CustomCooldown(1, 10, 1, 5, commands.BucketType.user, elements=getUserUpvoted()))
  async def tictactoe(self,ctx,user: discord.Member):
    if user == ctx.author:
        await ctx.reply("You can't play a game of TicTacToe with yourself, you moron.")
        raise Exception("ttt'ed self")
    elif user.bot:
        await ctx.send("You can't play TicTacToe with a bot, stupid.")
        raise Exception("ttt'ed bot")
    

    def getTurns():
      
      involved_users = [user.id, ctx.author.id]
      turn = random.randint(0,1)
      turnByTurn =[]
      for i in range(9):
        if turn+1 == 2:
          turn = -1
        turnByTurn.append(involved_users[turn+1])
        turn+=1
      return turnByTurn

    turn_list = getTurns()
    turn = 0
    userSquares =[]
    authorSquares =[]
    userwin = 0
    authorwin = 0
    variable = ""
    if turn_list[0] == user.id:
      variable = user.mention
    else:
      variable = ctx.author.mention
    turnNotif = await ctx.send(f"TicTacToe game between {user.name} and {ctx.author.name}\nYour turn {variable}")
    
    
    mainMessage = await ctx.send("\u200b",
        components = [ 
              [
                  Button(
                      label = "\u200b",
                      id = "a1",
                      style = ButtonStyle.grey,
                      
                  ),
                  Button(
                      label = "\u200b",
                      id = "a2",
                      style = ButtonStyle.grey,
                      
                  ),
                  Button(
                      label = "\u200b",
                      id = "a3",
                      style = ButtonStyle.grey,
                      
                  )
              ],
              [
                Button(
                      label = "\u200b",
                      id = "b1",
                      style = ButtonStyle.grey,
                      
                  ),
                  Button(
                      label = "\u200b",
                      id = "b2",
                      style = ButtonStyle.grey,
                      
                  ),
                  Button(
                      label = "\u200b",
                      id = "b3",
                      style = ButtonStyle.grey,
                  )
              ],
              [
                Button(
                      label = "\u200b",
                      id = "c1",
                      style = ButtonStyle.grey,
                      
                  ),
                  Button(
                      label = "\u200b",
                      id = "c2",
                      style = ButtonStyle.grey,
                      
                  ),
                  Button(
                      label = "\u200b",
                      id = "c3",
                      style = ButtonStyle.grey,
                  )
              ]
          ]

      )
      
    
      
    

    def success(squares):
      if "a1" in squares and "a2" in squares and "a3" in squares:
        return True
      if "b1" in squares and "b2" in squares and "b3" in squares:
        return True
      if "c1" in squares and "c2" in squares and "c3" in squares:
        return True
      if "a1" in squares and "b1" in squares and "c1" in squares:
        return True
      if "a2" in squares and "b2" in squares and "c2" in squares:
        return True
      if "a3" in squares and "b3" in squares and "c3" in squares:
        return True
      if "a1" in squares and "b2" in squares and "c3" in squares:
        return True
      if "a3" in squares and "b2" in squares and "c1" in squares:
        return True
      else: 
        return False
      
      

    while True:
        try:
              
              interaction = await self.bot.wait_for(
                  "button_click",
                  check = lambda i: i.component.id in ["a1", "a2","a3","b1","b2","b3","c1","c2","c3"] and i.channel.id == ctx.channel.id, 
                  timeout = 30.0 
              )
              if interaction.user.id != turn_list[turn]:
                await interaction.respond(type=4, content="It isn't your turn, idiot.", ephemeral=True)
              else:
                
                if turn_list[turn] == user.id:
                  userSquares.append(interaction.component.id)
                elif turn_list[turn] == ctx.author.id:
                  authorSquares.append(interaction.component.id)
                

                
                if success(userSquares) == True:
                  userwin = 1 
                if success(authorSquares) == True:
                  authorwin = 1
                else:
                  if turn != 8:
                    turn+= 1
                  else:
                    await asyncio.sleep(1)
                    await mainMessage.delete()
                    await ctx.send(f"You tied! Rip lol you suck.")
                    break
                
                

                labels = {}
                for id in ["a1", "a2","a3","b1","b2","b3","c1","c2","c3"]:
                  labels[id] = "\u200b"


                styles = {}
                for id in ["a1", "a2","a3","b1","b2","b3","c1","c2","c3"]:
                  styles[id] = ButtonStyle.grey

                disabled = {}
                for id in ["a1", "a2","a3","b1","b2","b3","c1","c2","c3"]:
                  disabled[id] = False


                for id in userSquares:
                  labels[id] = "X"
                  styles[id] = ButtonStyle.red
                  disabled[id] = True
                for id in authorSquares:
                  labels[id] = "O"
                  styles[id] = ButtonStyle.green
                  disabled[id] =True

                

                await interaction.respond(
                      
                      type = 7,
                      
                      components = [ 
                  [
                      Button(
                          label = labels["a1"],
                          id = "a1",
                          style = styles["a1"],
                          disabled = disabled["a1"]
                          
                      ),
                      Button(
                          label = labels["a2"],
                          id = "a2",
                          style = styles["a2"],
                          disabled = disabled["a2"]
                          
                      ),
                      Button(
                          label = labels["a3"],
                          id = "a3",
                          style =styles["a3"],
                          disabled = disabled["a3"]
                          
                      )
                  ],
                  [
                    Button(
                          label = labels["b1"],
                          id = "b1",
                          style = styles["b1"],
                          disabled = disabled["b1"]
                          
                      ),
                      Button(
                          label = labels["b2"],
                          id = "b2",
                          style = styles["b2"],
                          disabled = disabled["b2"]
                          
                      ),
                      Button(
                          label = labels["b3"],
                          id = "b3",
                          style = styles["b3"],
                          disabled = disabled["b3"]
                      )
                  ],
                  [
                    Button(
                          label = labels["c1"],
                          id = "c1",
                          style = styles["c1"],
                          disabled = disabled["c1"]
                          
                      ),
                      Button(
                          label = labels["c2"],
                          id = "c2",
                          style = styles["c2"],
                          disabled = disabled["c2"]
                          
                      ),
                      Button(
                          label = labels["c3"],
                          id = "c3",
                          style = styles["c3"],
                          disabled = disabled["c3"]
                      )]])
              
                if userwin == 1:
                  await asyncio.sleep(1)
                  await mainMessage.delete()
                  await ctx.send(f"{user.name} wins this round!")
                  break
                if authorwin == 1:
                  await asyncio.sleep(1)
                  await mainMessage.delete()
                  await ctx.send(f"{ctx.author.name} wins this round!")
                  break
                
                variable = ""
                if turn_list[turn] == user.id:
                  variable = user.mention
                else:
                  variable = ctx.author.mention

                await turnNotif.edit(f"TicTacToe game between {user.name} and {ctx.author.name}\nYour turn {variable}")
                
        

        except asyncio.TimeoutError:
          
          await ctx.send("You ran out of time.")
          
          await mainMessage.delete()
          break

        

  @commands.command()
  @commands.bot_has_guild_permissions(add_reactions = True)
  @commands.check(CustomCooldown(1, 10, 1, 5, commands.BucketType.user, elements=getUserUpvoted()))
  async def vocabularygame(self,ctx):
    
    

    wait = await ctx.reply("Please wait...")
    file = open("./json/words.txt","r")
    words = file.readlines()
    listWords =[]
    for word in words:
    
      word = word[:-1]
      word = word.lower()
        
      listWords.append(word) 

    freq ={}
    for word in listWords:
      

      try:
        freq[word] +=1
      except KeyError:
        freq[word] = 1

    listWords = list(freq)
    for word in listWords:
      if len(word) == 1:
        listWords.remove(word)

    vowels = ["a","e","i","o","u"]
    randomLetters = ''.join(random.choices(string.ascii_lowercase,k=7))
    for i in range(3):
      randomLetters = randomLetters + vowels[random.randint(0,4)]
    await wait.edit(f"With the letters ``{randomLetters}`` type as many words as you can within 30s!")
    
    reqLetters= list(randomLetters)
    
    def check(str,set):
      reqLetters = sorted(set)
      
      
      try:
        for c in list(str):
          
          reqLetters.remove(c)
      except ValueError:
        return False
      return True
    
      
    

    def backgroundVocab():
      global timerVocab
      timerVocab = 30
      while True:
        time.sleep(1)
        timerVocab -= 1
        if timerVocab == 0:
          break
      
    
    
    threading.Thread(name='backgroundVocab', target=backgroundVocab).start()
    score = 0                             
    combo = 0
    maxcombo = 0
    accuracy = 0
    correct = 0
    used_words = []
    d = 0
    
    while timerVocab != 0:
      
      
      try:

        msg = await self.bot.wait_for(
        "message",
        check = lambda i: i.author.id == ctx.author.id and i.channel.id == ctx.channel.id, 
        timeout = timerVocab
      )
        

        
        if msg.content in listWords and msg.content not in used_words and check(msg.content,reqLetters) == True:
          
          await msg.add_reaction("✅")
          used_words.append(msg.content)
          correct +=1
          score += 100
          combo += 1
          if maxcombo < combo:
            maxcombo+=1
          
          score+= combo*25
        elif check(reqLetters,msg.content) == False or msg.content not in listWords:
          used_words.append(msg.content)
          combo = 0
          
        
        
        
      except asyncio.TimeoutError:
        break
    try:
      accuracy = correct/len(used_words)
    except ZeroDivisionError:
      accuracy = 0
    d = score*(accuracy/8)
    score +=d
        
      
      
      
    color = int(await colorSetup(ctx.message.author.id),16)
    em = discord.Embed(color=color)
    em.add_field(name = "``Stats``",value=f"Accuracy: {math.ceil(accuracy*100)}%\nNumber of correct words: {correct}\nMax combo: {maxcombo}\nAccuracy bonus: +{math.ceil(d)}\n**Total score: {math.ceil(score)}**",inline=False)
    await ctx.send(embed = em)
    
    
        
    
    
  
  @commands.command()
  @commands.check(CustomCooldown(1, 10, 1, 5, commands.BucketType.user, elements=getUserUpvoted()))
  async def typingrace(self,ctx):
    
    
   
    instructions = await ctx.send("Typing race will start!\nPress the button to join!", 
    components = [
      [
        Button(
          label = "Join",
          id = "join",
          style = ButtonStyle.green
          ),
          Button(
          label = "Start",
          id = "start",
          style = ButtonStyle.blue
          )
        ]])
        
    players = []
    
    
    while True:
      
      try:
        interaction = await self.bot.wait_for(
                  "button_click",
                  check = lambda i: i.component.id in["join","start"] and i.channel.id == ctx.channel.id, 
                  timeout = 60.0 
              )
        if interaction.component.id == "start" and len(players) == 0:
          await instructions.delete()
          await ctx.send("I guess no one wants to join the game.")
          raise Exception("no on")
        if interaction.user.id not in players and interaction.component.id == "join":
     
          players.append(interaction.user.id)
        
          await interaction.respond(type=4, content="You successfully joined the game!", ephemeral=True)
        elif interaction.component.id == "start":
          await instructions.delete()
          break
        else:
          await interaction.respond(type=4, content="You've already joined the game, idiot.", ephemeral=True)
          
        
        
      except asyncio.TimeoutError:
        await instructions.delete()
        await ctx.send("I guess no one wants to join or start the game.")
      
    
    def backgroundTyping():
      global timerTyping
      timerTyping = 180
      while True:
        time.sleep(1)
        timerTyping -= 1
        if timerTyping == 0:
          break
    
    
    threading.Thread(name = 'backgroundTyping', target = backgroundTyping).start()
    await ctx.send("Type the sentence below!")
    texts = [
      "She could hear him in the shower singing with a joy she hoped he'd retain after she delivered the news.",
      "We have young kids who often walk into our room at night for various reasons including clowns in the closet.",
      "She had that tint of craziness in her soul that made her believe she could actually make a difference.",
      "When I cook spaghetti, I like to boil it a few minutes past al dente so the noodles are super slippery.",
      "He felt that dining on the bridge brought romance to his relationship with his cat.",
      "She couldn't decide of the glass was half empty or half full so she drank it.",
      "The urgent care center was flooded with patients after the news of a new deadly virus was made public.",
      "The Tsunami wave crashed against the raised houses and broke the pilings as if they were toothpicks.",
      "The complicated school homework left the parents trying to help their kids quite confused.",
      "The battle over coal continued to rage Tuesday afternoon during a hearing held by the House Oversight and Investigations Subcommittee on the community impacts of impending Environmental Protection Agency regulations for power plants.",
      "They want a presidential nominee who fights for them, and who is pitching a fresh and dramatic plan for improving their lives in immediate, concrete ways.",
      "Gowdy's letter comes a day after a senior State official told Gowdy in a letter that Finer's appearance 'will not be possible' and that State 'cannot participate' in a hearing Gowdy's staff suggested holding next week.",
      "In Chicago, a regional housing authority that covers eight counties, including Cook County, is working to move families from the inner city to higher-opportunity neighborhoods.",
      "Meanwhile, here is the Lorne Michaels-backed show I wish had lasted for 40 years, or at least more years than it did: the Toronto-based Kids in the Hall.",
      "Lillian, Kimmy's hippie-haired landlady, is making stilted peace with the fact that the only home she has ever known—her New York neighborhood—is rapidly evolving away from her.",
      "Johnson, the Chicago native joined Marathon Pharmaceuticals, which specializes in making drugs for hard-to-treat ailments most people have never heard of.",
      "My avowed purpose in composing that text, as any swot who has suffered the Duty and Dullness rampant in our Schools must know, was to employ my modest pen as a scourge against human Folly and the vanities of the Age.",
      "How do you think about distinguishing between intellectual curiosity and commercial intent -- or, I guess, between different forms of interest?",
      "If there's been one overarching theme to the Republican presidential primary in the last week or two, it's been that past coming back to haunt the contenders.",
      "A growing body of literature now suggests that the earlier we turn back the clock in kids’ development, the more profound the impact of their environment.",
      "The rise in popularity of the more violent sport of American football over the past forty years may reflect shifts in militaristic ideology, from the Cold War to current overseas conflicts.",
      "There is some fun gossip: I didn't know, for example, that show-runner Matthew Weiner started working on the landmark drama while co-writing for Becker."
      ]
    
    random_text = texts[random.randint(0,len(texts)-1)]
    shown_text = random_text.replace("","\u200b")
    await ctx.send(f"``{shown_text}``")
    accuracy = 0
    wpm = 0 
    penalty = 0
    leaderboards = {}
    while timerTyping != 0:
      try:
        msg = await self.bot.wait_for(
        "message", check = lambda i: i.author.id in players and i.channel.id == ctx.channel.id,timeout = timerTyping)
        
        def checkAccuracy(j):
          correct = 0
          accuracy = 0
          a = random_text.split(" ")
          b = j.split(" ")
          
          for i in range(len(a)):
            try:

              if b[i] == a[i]:
                correct += 1
            except:
              pass
              
          accuracy = correct/len(a)
          return accuracy
          
        players.remove(msg.author.id)

        accuracy = checkAccuracy(msg.content) 
        
        wpm = len(msg.content)/(180-timerTyping)
        penalty = wpm*(1-accuracy)
        wpm -= penalty
  
        leaderboards[msg.author.name] = wpm
        
        color = int(await colorSetup(msg.author.id),16)
        em = discord.Embed(color = color)
        
        em.add_field(name = "``stats``", value = f"Characters/second: {round(len(msg.content)/(180-timerTyping),2)}\nAccuracy: {round(accuracy*100,2)}%\nInaccuracy penalty: -{round(penalty,2)}\n**Final score: {round(wpm,2)}**")
        await msg.reply(embed = em)
        if len(players) == 0:
          break
      except asyncio.TimeoutError:
        break
    leaderboards = str(sorted(leaderboards.items(), key = lambda kv:(kv[1], kv[0]),reverse = True))[1:-1]
    
    leaderboards = leaderboards.split(")")
    newLeaderboards=[]
    for l in leaderboards:
      h = l[1:].replace(",",": ").replace("'","").replace("(","")
      newLeaderboards.append(h)
      
      if l == '':
        newLeaderboards.remove(l)
    finalText = ""
    for l in newLeaderboards:
      
      finalText = finalText+"\n"+l
    color = int(await colorSetup(ctx.author.id),16)
    em2 = discord.Embed(color = color)
    em2.add_field(name = "``Leaderboard``",value = finalText,inline = False)
    await ctx.send(embed = em2)




  @commands.command(name = "wouldyourather",aliases = ["wyr"])
  @commands.check(CustomCooldown(1, 10, 1, 5, commands.BucketType.user, elements=getUserUpvoted()))
  async def wouldyourather(self,ctx):
   
    option1= [
      "lose a car",
      "have the ability to see 10 minutes into the future",
      "have telekinesis",
      "be in a coma for 10 years",
      "lose your vision",
      "find a cockroach in your bed",
      "drink from a toilet bowl",
      "become vegan",
      "always lie",
      "speak any language",
      "eat someone's vomit",
      "let somebody read your DMs",
      "drink pee",
      "only eat raw food",
      "be able to tell the future",
      "have US$1 million now",
      "clean the toilet with a toothbrush",
      "be reincarnated as a plant",
      "be always criticized",
      "get 10 books free",
      "know when you are going to die",
      ]
    option2 =[
      "lose all the pictures you have ever taken",
      "have the ability to see 150 years into the future",
      "have telepathy",
      "be jailed for 5 years",
      "lose all memories",
      "find some strange white sticky stuff on your bed",
      "eat from the trashcan",
      "cannabalise people you see",
      "always tell the truth",
      "speak to animals",
      "drink someone's blood",
      "let somebody see your camera roll",
      "brush teeth with solid fuel",
      "only eat expired food",
      "be able to recall your past with perfect clarity",
      "have US$5 000 every week for the rest of your life",
      "lick the floor",
      "be reincarnated as a mosquito",
      "be always ignored",
      "get to watch 1 movie free",
      "know how you are going to die",
      ]
      
    randomQnNo = random.randint(0,len(option1)-1)
    options = (option1[randomQnNo],option2[randomQnNo])
    
    color = int(await colorSetup(ctx.message.author.id),16)
    em = discord.Embed(color = color)
    em.add_field(name = "Would you rather...", value = f"1. {options[0]}\n2. {options[1]}",inline = False)
    em.set_footer(text = "Best played in a voice call!")
    embed1= await ctx.send(embed = em)
    interaction = await ctx.send("You have 30s to select one of the below!", 
    components = [
      [
        Button(
          label = "Option 1",
          id = "1",
          style = ButtonStyle.green
          ),
          Button(
          label = "Option 2",
          id = "2",
          style = ButtonStyle.blue
          )
        ]])
        
    def backgroundWYR():
      global timerWYR
      timerWYR= 30
      while True:
        time.sleep(1)
        timerWYR -= 1
        if timerWYR == 0:
          break
      
    
    
    threading.Thread(name='backgroundWYR', target=backgroundWYR).start()
    respondents = []
    voted1 = 0 
    voted2 = 0 
    totalvoted = 0
    while timerWYR !=0:
      
      try:
        click = await self.bot.wait_for(
                  "button_click",
                  check = lambda i: i.component.id in["1","2"] and i.channel.id == ctx.channel.id and i.message.id == interaction.id, 
                  timeout = timerWYR
                )
                
                
        if click.user.id not in respondents:
          
          totalvoted +=1
        
          await click.respond(type=4, content=f"You voted for option {click.component.id}!", ephemeral=True)
        elif click.user.id in respondents:
          await click.respond(type=4, content=f"You've already voted, you {insults.long_insult()}. ", ephemeral=True)
          
          
        
        if click.component.id == "1" and click.user.id not in respondents:
          respondents.append(click.user.id)
          voted1 += 1
        elif click.component.id== "2" and click.user.id not in respondents:
          respondents.append(click.user.id)
          voted2 +=1
        
        
      except asyncio.TimeoutError:
        await interaction.delete()
        await embed1.delete()
        break
      
    em2 = discord.Embed(color = color)
    try:
      em2.add_field(name = "Results!", value = f"``{(voted1/totalvoted)*100}%`` {options[0]}\n``{(voted2/totalvoted)*100}%`` {options[1]}",inline = False)
    except ZeroDivisionError:
      em2.add_field(name = "Results!", value = f"``0%`` {options[0]}\n``0%`` {options[1]}",inline = False)
    em2.set_footer(text = "Best played in a voice call!")
    await ctx.send(embed = em2)
      


  @commands.command(name="tord",aliases = ["truthordare"])
  @commands.check(CustomCooldown(1, 10, 1, 5, commands.BucketType.user, elements=getUserUpvoted()))
  async def truthordare(self,ctx):
    color = int(await colorSetup(ctx.message.author.id),16)

    
    interaction = await ctx.send("Truth or dare?",
    components = [
      [
        Button(
          label = "Truth",
          id = "0",
          style = ButtonStyle.green
          ),
          Button(
          label = "Dare",
          id = "1",
          style = ButtonStyle.red
          )
        ]])
    
    try:
      click = await self.bot.wait_for("button_click",
      check = lambda i: i.component.id in["0","1"] and i.channel.id == ctx.channel.id and i.message.id == interaction.id, 
        timeout = 30.0)
      if click.component.id == "0":
        
        arr = []
        with open("./json/TorD.csv",newline="") as file:
          reader = csv.DictReader(file)
          for row in reader:
            arr.append(row)
            
        
        def choose():
          while True:
            ran = random.randint(0,len(arr)-1)
          
            if arr[ran]["type"] == "0":
            
              break
          return arr[ran]["content"]
            
        color = int(await colorSetup(ctx.message.author.id),16)
       
        em = discord.Embed(color = color, title = "Truth", description = choose())
        em.set_footer(text = "imagine being a pussy")
        
        await interaction.delete()
        a= await ctx.send(embed = em)
        b= await ctx.send("\u200b",
        components = [[
        Button(
          label = "Reroll!",
          id = "reroll",
          style = ButtonStyle.green
          )]]
          )
        
         
        reroll = await self.bot.wait_for(
          "button_click",
          check =lambda i: i.component.id =="reroll" and i.channel.id == ctx.channel.id, 
          timeout = None
        )
          
        
        em2 = discord.Embed(color = color, title = "Truth", description = choose())
        em2.set_footer(text = "imagine being a pussy")
        await a.edit(embed = em2)
        await b.delete()
        
        
        
        
        
        
        
        #fmlfmlfmlfmflmflfmlfmflmflmflfmlfmlfmflmfl
      elif click.component.id == "1":

        arr = []
        with open("./json/TorD.csv",newline="") as file:
          reader = csv.DictReader(file)
          for row in reader:
            arr.append(row)
            
        
        def choose():
          while True:
            ran = random.randint(0,len(arr)-1)
          
            if arr[ran]["type"] == "1":
            
              break
          return arr[ran]["content"].replace(";",",")
            
        color = int(await colorSetup(ctx.message.author.id),16)
       
        em = discord.Embed(color = color, title = "Dare", description = choose())

        
        await interaction.delete()
        a= await ctx.send(embed = em)
        b= await ctx.send("\u200b",
        components = [[
        Button(
          label = "Reroll!",
          id = "reroll",
          style = ButtonStyle.green
          )]]
          )
        
         
        reroll = await self.bot.wait_for(
          "button_click",
          check =lambda i: i.component.id =="reroll" and i.channel.id == ctx.channel.id, 
          timeout = None
        )
          
        
        em2 = discord.Embed(color = color, title = "Dare", description = choose())
        
        await a.edit(embed = em2)
        await b.delete()
    except asyncio.TimeoutError:
      pass
   
    


def setup(bot):
  bot.add_cog(Games(bot))