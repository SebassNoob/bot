
import discord
from discord.ext import commands

  @commands.cooldown(1,30)
  @commands.command()
  async def spam(self,ctx,num,*spams):
      response = ''
      if str(num).isdigit() == False:
          
        await ctx.send("This is how to format, stupid:\n```$spam[num of times to spam][spam content]```")
      elif int(num) > 15:
        await ctx.send("Yeah not sorry my arse can't handle that much.\nAsk for 25 or less.")

      if str(num).isdigit() == True and int(num) <= 25:
        for spam in spams:
          response = response +" "+ spam

        uid = ctx.author.id
        status = await familyFriendlySetup(uid)
        if status == True:
          response =  await changeff(response)
        else:
          pass
        mArr = []
        await ctx.send("Now spamming `"+response+"`. \n`stop` to stop spam.")
      def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ['stop']
      for i in range(int(num)):
        try:
        
          m = await ctx.send(response)
          
          mArr.append(m.id)
          msg = await self.bot.wait_for("message",timeout=1.5,check=check)
          
          if msg:
            await ctx.reply("Stopped.")
            break
            raise Exception
          
        except asyncio.TimeoutError:
          continue
      await asyncio.sleep(60)
      for c in mArr:
        self.bot.http.delete_message(ctx.channel.id, c)

