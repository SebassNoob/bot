import discord
from discord.ext import commands
import os 

from other.asyncCmds import colorSetup, familyFriendlySetup,changeff,getDataU,addDataU,postTips

import random
import json


from other.customCooldown import CustomCooldown
from other.upvoteExpiration import getUserUpvoted


class MainFeatures(commands.Cog):
  
  def __init__(self, bot):
        self.bot = bot

         
  @commands.command(name = 'roast', aliases = ['burn'])
  @commands.check(CustomCooldown(1, 6, 1, 3, commands.BucketType.user, elements=getUserUpvoted()))
  async def roast(self,ctx,userToRoast : discord.Member= None):
      
        
        roastList1 =["Your face makes onions cry.","Light travels faster than sound, which is why you seemed bright until you spoke.","Those penis enlargement pills must be working — you’re twice the dick you were yesterday."," I treasure the time I don’t spend with you.","You’re entitled to your incorrect opinion.","I’d smack you, but that would be animal abuse.","Your birth certificate is an apology letter from the condom factory.","You must have been born on a highway because that's where most accidents happen.","Stop trying to be a smart ass, you're just an ass.","Why don't you slip into something more comfortable... like a coma."]
        roastList2=["Shock me, say something intelligent.","How old are you? - Wait I shouldn't ask, you can't count that high.","Have you been shopping lately? They're selling lives, you should go get one.","If I told you that I have a piece of dirt in my eye, would you move?","Stupidity is not a crime so you are free to go.","We can always tell when you are lying. Your lips move.","Are you always this stupid or is today a special occasion?","Don't you have a terribly empty feeling - in your skull?","Seriously? You were the sperm that won!?","Is your ass jealous of the amount of shit that came out of your mouth?"]
        roastList3 = ["You are much like a cloud. When you disappear, its a beautiful day.","You should introduce your upper lip to your lower lip sometime and shut up.", "Zombies eat brains. You're safe however.","I was going to give you a nasty look, but I see you already have one.","There is no need to repeat yourself. I'd ignored you just fine the first time.","Keep rolling your eyes. One day you'll find a brain back there.","When I see your face, there's not a thing that I would change...Except for the direction in facing.","The problem with you is that your mouth is moving.","I hope the rest of your day is as unpleasent as you are.","You have the rest of your life to be a jerk, please take today off."]
        roastList4 = ["Were you born this stupid or did you take lessons?","The people who tolerate you on a daily basis are the real heroes.","You look like something that came out of a slow cooker.","I thought of you today. It reminded me to take out the trash.","You are so full of shit, the toilet’s jealous.","Too bad you can’t Photoshop your ugly personality.","Do your parents even realize they’re living proof that two wrongs don’t make a right?","You’re like the end pieces of a loaf of bread. Everyone touches you, but nobody wants you.","You are more disappointing than an unsalted pretzel."," If laughter is the best medicine, your face must be curing the world."]
        randomRoast = roastList1[random.randint(0,9)]
        randomRoast2 = roastList2[random.randint(0,9)]
        randomRoast3 = roastList3[random.randint(0,9)]
        randomRoast4 = roastList4[random.randint(0,9)]
        roastArray = [randomRoast,randomRoast2,randomRoast3,randomRoast4]
        finalRoast = roastArray[random.randint(0,3)]
        
        uid = ctx.author.id
        status = await familyFriendlySetup(uid)
        if status ==True:
          finalRoast =  await changeff(finalRoast)
            
      

        if userToRoast != '' and userToRoast!= None:
          await ctx.send(' {}'.format(userToRoast.mention))
        color = int(await colorSetup(ctx.message.author.id),16)
        embedVar = discord.Embed( color=color)
        embedVar.set_author(name="Roast from"+' {}'.format(ctx.author), icon_url = ctx.author.avatar_url)
          
        embedVar.add_field(name="\u200b", value=finalRoast, inline=False)
        embedVar.set_footer(text="u suck")
        tip = postTips()
        
        if tip != None:
          
          await ctx.send(tip)
        await ctx.send(embed=embedVar)


  
  
  @commands.command()
  @commands.check(CustomCooldown(1, 6, 1, 3, commands.BucketType.user, elements=getUserUpvoted()))
  async def swear(self,ctx):
    
        swearList = ["You cow.","You bloody bitch.", "You freaking arsehole.","You ranky danky piece of dogshit.",'You little prick.','You twithead.',"You donkey shit.","You filthy poohead.","You absolute moron.","You actual idiot.","You talkative brat.","You stupid donghead.","You fucking loser","You twatface","You dirty asshole."]
        randomSwear = swearList[random.randint(0,14)]


        uid = ctx.message.author.id
        status = await familyFriendlySetup(uid)
        if status ==True:
          randomSwear =  await changeff(randomSwear)
        color = int(await colorSetup(ctx.message.author.id),16)
        embedVar2 = discord.Embed(color =color)
        embedVar2.add_field(name = randomSwear, value = "\u200b",inline = False)
        embedVar2.set_footer(text="requested by " +'{}'.format(ctx.message.author))
        tip = postTips()
        
        if tip != None:
          
          await ctx.send(tip)
        await ctx.send(embed=embedVar2)
      

        

  
  @commands.command(name = 'urmom' , aliases = ["yourmom"])
  @commands.check(CustomCooldown(1, 6, 1, 3, commands.BucketType.user, elements=getUserUpvoted()))
  async def urmom(self,ctx):
    
        urmomList = ["Yo momma is so fat when she got on the scale it said, 'I need your weight not your phone number.'","Yo mamma is so ugly when she tried to join an ugly contest they said, 'Sorry, no professionals.'","Yo momma's so fat and old when God said, 'Let there be light,' he asked your mother to move out of the way.","Yo momma's so fat, that when she fell, no one was laughing but the ground was cracking up.","Yo momma is so fat that Dora can't even explore her!","Yo momma so stupid she stuck a battery up her ass and said, 'I GOT THE POWER!'","Yo momma is so hairy, when she went to the movie theater to see Star Wars, everybody screamed and said, 'IT'S CHEWBACCA!'","Yo mamma is so fat she doesn't need the internet, because she's already world wide.","Yo mama so ugly when she went into a haunted house she came out with a job application.","Your momma's so ugly, when she goes into a strip club, they pay her to keep her clothes on."]
        urmomList2 = ["Your mom so fat, when a car tried to swerve to avoid her, it took 17 years to complete said swerve.","Your mom is so gassy that when she farts, the amount of methane in the atmosphere triples.","Your mom so idiotic, that when she took an iq test, the iq score came out negative.","Your mom so stupid, when she tried spelling, she spelt her name as 'idiot'.","Yo mama's so fat, she can't even jump to a conclusion.","Yo mama's so stupid, she stared at a cup of orange juice for 12 hours because it said 'concentrate.'","Yo mama's so stupid, when they said, 'Order in the court,' she asked for fries and a shake.","Yo mama's so stupid, when I told her that she lost her mind, she went looking for it.","Yo mama's so stupid, she went to the dentist to get a Bluetooth.","Yo mama's so ugly, she made a blind kid cry."]
        urmomList3 = ["Your momma so poor, she ate cereal with a fork in order to save milk.","Yo momma so stupid, she stole a free sample.","Your momma so fat, her belt size is the equator's diameter.","Yo momma so stupid she put paper on the television and called it paper(pay-per) view.","Yo momma so stupid, she returned a donut to the store because it had a hole in it.","Your mom so nasty, she bit a dog and gave it rabies.","Yo momma so ugly that when she threw a boomerang, it didn't want to come back.","Yo momma so stupid that she puts lipstick on her forehead to make up her mind.","Your mom so old that when people told her to act her own age, she died.","Yo momma so ugly her pillow cries at night."]
        randomUrmom = urmomList[random.randint(0,9)]
        
        
        randomUrmom2 = urmomList2[random.randint(0,9)]
        randomUrmom3 = urmomList3[random.randint(0,9)]
        urmomArray = [randomUrmom,randomUrmom2,randomUrmom3]
        finalUrmom = urmomArray[random.randint(0,2)]
        color = int(await colorSetup(ctx.message.author.id),16)


        uid = ctx.author.id
        status = await familyFriendlySetup(uid)
        if status ==True:
          finalUrmom =  await changeff(finalUrmom)

        embedVar3 = discord.Embed(color = color)
        embedVar3.add_field(name = finalUrmom, value = "\u200b",inline = False)
        embedVar3.set_footer(text="requested by " +'{}'.format(ctx.message.author)+"\nimagine having a mom.")
        tip = postTips()
        
        if tip != None:
          
          await ctx.send(tip)
        await ctx.send(embed=embedVar3)


 
  @commands.command(name = "uninspire", aliases = ["uninspirational"])
  @commands.check(CustomCooldown(1, 6, 1, 3, commands.BucketType.user, elements=getUserUpvoted()))
  async def uninspire(self,ctx):
    uninspireList = ["It's never too late to go back to bed.","It takes 37 muscles to frown but 0 muscles to shut the fuck up.","Looking at inspirational quotes to feel better is like looking at a treadmill to lose weight.","Instagram is a great place to look at pictures of the fake lives of all the people you hate.","Before you judge someone else, try to remember that you are also a piece of shit.","If you never believe in yourself, you'll never let yourself down.","True love is when 2 people lower their standards to just the right amount.","Relationships are like wine. They are expensive and eventually you just end up with a headache.","Monday hates you too.","Getting out of bead is almost always the wrong decision.", "The little progress you make today will be lost when you die.","Mistakes are a fact of life, which is why you should never try.","Success is a dream most of us will never achieve.","Today is going to be worse than yesterday.","Go the extra mile and you'll probably be run over by a truck.","Life has 2 rules:\n#1: Always quit when you can.\n#2: REMEMBER THE FIRST RULE","You're much weaker than you think you are.","You are going to give up today.","Strive for as little progress as you can.","In the middle of difficulty lies a hole all the way to hell."]
    finalUninspire = uninspireList[random.randint(0,19)]
    color = int(await colorSetup(ctx.message.author.id),16)

    uid = ctx.author.id
    status = await familyFriendlySetup(uid)
    if status ==True:
      finalUninspire =  await changeff(finalUninspire)


    embedVar3 = discord.Embed(color = color)
    embedVar3.add_field(name = finalUninspire, value = "\u200b",inline = False)
    embedVar3.set_footer(text="requested by " +'{}'.format(ctx.message.author))
    tip = postTips()
        
    if tip != None:
          
      await ctx.send(tip)
    await ctx.send(embed=embedVar3)
  
  
  @commands.command()
  @commands.check(CustomCooldown(1, 10, 1, 5, commands.BucketType.user, elements=getUserUpvoted()))
  async def dmthreaten(self,ctx, user: discord.Member, *args):
    
    users = await getDataU()
    uid = user.id
    async def command():
      threat = ""
      for arg in args:
        threat = threat + " "+arg
      author_name = '{}'.format(ctx.author)
      if threat == "":
        t = ["I'm gonna find you and shove a pencil up yo ass.","Get out of here, or imma yeet you off a cliff irl.","I'm gonna go to your house and shit inside of it.","I'll stalk you in your dreams","Don't you dare cross me, or I will whoop your ass","I'm going to leave a bunch of dogshit on your desk tomorrow.","Watch out, I've hired a bunch of goons to intimidate you as they stare into your window.","I'm gonna steal EVERYTHING from your fridge","I'm going to kidnap your virginity and hold it ransom","I'm going to vomit on your cat."]
        threat = t[random.randint(0,9)]

      channel = await user.create_dm()
      color = int(await colorSetup(ctx.message.author.id),16)
      em = discord.Embed(color = color)
      em.set_author(name = author_name+"'s threat",icon_url = ctx.author.avatar_url)
      em.add_field(name="\u200b",value=threat,inline=False)
      await channel.send(embed = em)
      tip = postTips()
        
      if tip != None:
          
        await ctx.send(tip)
      await ctx.send("The user has been sent a threat in dms.")
    
    try:
      if users[str(uid)]["dmblocker"] == 0:
        await command()

        
      elif users[str(uid)]["dmblocker"] ==1:
        tip = postTips()
        print(tip)
        if tip != None:
          
          await ctx.send(tip)
        await ctx.send("Sorry, the user you mentioned doesn't want to be dm'ed by me ;(")
    except:
      await addDataU(uid)
      await command()




def setup(bot):
    bot.add_cog(MainFeatures(bot))