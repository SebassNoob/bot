import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import asyncio
import random
import json
import string
from other.asyncCmds import colorSetup
from other.customCooldown import CustomCooldown
from other.upvoteExpiration import getUserUpvoted
import threading
from threading import Thread
import time
import math

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
                    type = InteractionType.UpdateMessage,
                    
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
                  check = lambda i: i.component.id in ["a1", "a2","a3","b1","b2","b3","c1","c2","c3"], 
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
                      type = InteractionType.UpdateMessage,
                      
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

    expectedTime = ((level*level+1)/2)*5
    
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
                  check = lambda i: i.component.id in ["a1", "a2","a3","b1","b2","b3","c1","c2","c3"], 
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
                  turn+= 1
                  
                
                

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
                      
                      type = InteractionType.UpdateMessage,
                      
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
          break
          await ctx.send("You ran out of time.")
          
          await mainMessage.delete()

        

  @commands.command()
  @commands.bot_has_guild_permissions(add_reactions = True)
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

    randomLetters = ''.join(random.choices(string.ascii_lowercase,k=10))
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
    while True:
      try:
        msg = await self.bot.wait_for(
        "message",
        check = lambda i: i.author.id == ctx.author.id, 
        timeout = 30.0 
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
          
          
        

        if timerVocab <= 0:
          accuracy = correct/len(used_words)
          d = score*(accuracy/8)
          score +=d
          break
      except asyncio.TimeoutError:
        break
      
      
    color = int(await colorSetup(ctx.message.author.id),16)
    em = discord.Embed(color=color)
    em.add_field(name = "``Stats``",value=f"Accuracy: {math.ceil(accuracy)*100}%\nNumber of correct words: {correct}\nMax combo: {maxcombo}\nAccuracy bonus: +{math.ceil(d)}\n**Total score: {math.ceil(score)}**",inline=False)
    await ctx.send(embed = em)
    
    
        
    
    

    
   
    
              



def setup(bot):
  bot.add_cog(Games(bot))