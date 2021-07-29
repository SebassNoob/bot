import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import asyncio
import random
from other.asyncCmds import colorSetup

class Games(commands.Cog):
  
  def __init__(self, bot):
        self.bot = bot

  @commands.command()
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
      
      while True:
        try:
              interaction = await self.bot.wait_for(
                  "button_click",
                  check = lambda i: i.component.id in ["a1", "a2","a3","b1","b2","b3","c1","c2","c3"], 
                  timeout = 30.0 
              )

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
          await asyncio.sleep(1)
          break

    
    await mainMessage.delete()
    await a.delete()
    await ctx.send(f"Your score: {level}")
    
  @commands.command()
  async def tictactoe(self,ctx,user: discord.Member):
    involved_users = [user.id, ctx.author.id]
    pass
def setup(bot):
  bot.add_cog(Games(bot))