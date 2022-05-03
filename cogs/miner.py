import discord
import resource
import user
from replit import db
from cogs.error import UserNotInDb
from discord.ext import commands
from discord.ui import Button, Select, View

cooldowns = dict()
registeredviews = list()
currentview = None

class endinteractionbtn(Button):
  def __init__(self, row=1):
    super().__init__(label="End Interaction")
    
  async def callback(self, interaction):
    await currentview.disable_all()
    await       interaction.response.edit_message(view=currentview)
  
def initialize_cooldowns(kooldowns):
  for i in db["users"]:
    user_id = i
    duration = 17.5
    kooldowns[user_id] = commands.CooldownMapping.from_cooldown(1, duration, commands.BucketType.user)


class view_timeout(View):
  def __init__(self, ctx, timeout=10):
    super().__init__(timeout=timeout)
    self.register()
    self.inactive = False
    self.ctx = ctx
   
  async def on_timeout(self):
    if self.inactive == False:
      for i in self.children:
        i.disabled=True
      await self.message.edit(view=self)


  async def interaction_check(self, interaction: discord.Interaction):
    if interaction.user != self.ctx.author:
      await interaction.response.send_message("That's not your miner bro", ephemeral=True)
      return False
    else:
      return True

  def register(self):
    registeredviews.append(self)

  def setactive(self):
    for i in registeredviews:
      i.inactive = True
    self.inactive = False
    return self

  async def disable_all(self):
    for i in self.children:
      i.disabled = True


class Miner(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    initialize_cooldowns(cooldowns)
    self.item = resource.Item()
    self.goback = list()
    self.allitems = self.item.getallitems()


  def check_cooldown():
    async def predicate(ctx):
      user_id = str(ctx.author.id)
      if user_id == "895289342497538059":
        return True
      else:
        if user_id in cooldowns:
          bucket = cooldowns[user_id].get_bucket(ctx.message)
          retry_after = bucket.update_rate_limit()
          if retry_after:
            raise commands.CommandOnCooldown(bucket, retry_after, commands.BucketType.user)
        else:
          raise UserNotInDb(ctx.author)
        return True

    return commands.check(predicate)

  def check_if_in_db():
    async def predicate(ctx):
      usr = user.User(ctx.author)
      if not await usr.check_if_in_db():
        raise UserNotInDb(ctx.author)
      return True
    return commands.check(predicate)

 
    
  @commands.command(name="distribution", aliases=["dist"])
  async def distrubution(self, ctx):
    embed = discord.Embed(title="Miner Ore Distributing Chart", color=discord.Colour.random())
    embed.set_image(url="https://i.ibb.co/Rg90Qnn/b3bak5eige381-png.png")
    await ctx.reply(embed=embed, mention_author=False)


  
  @commands.command(name="mine", aliases=["dig"])
  @check_cooldown()
  @check_if_in_db()
  async def mine(self, ctx):
    embed = await resource.mine_loot(ctx.author)
    await ctx.reply(embed=embed, mention_author=False) 

  
  
  @commands.command(name="returntobase", aliases=["rtb"])
  async def returntobase(self, ctx):
    usr = user.User(ctx.author)
    if await usr.returntobase():
      await ctx.send("You Successfully returned to base!", ephemeral=True)            
    else:
      await ctx.send("You are already in your base lol", ephemeral=True)
   
      
    

    
  @commands.command(name="inventory",aliases=["inv"])
  @check_if_in_db()
  async def inventory(self, ctx):  
    usr = user.User(ctx.author)   
    embed = discord.Embed(title=f"{ctx.author.name}'s inventory", color=discord.Colour.random())
    invdict = await usr.get_user_data("inventory")
    for i in invdict:
      if invdict[i] != 0:
        name = self.allitems[i]["name"]
        id = self.allitems[i]["id"]
        catagory = self.allitems[i]["catagory"]
        embed.add_field(name=f"{id} {name} ─ {invdict[i]}", value=f"*ID* `{i}` ─ {catagory}", inline=False)
    embed.set_footer(text="yes")
    await ctx.send(embed=embed)

  @commands.command(name="createaccount", aliases=["start", "create"])
  async def createaccount(self, ctx):
    usr = user.User(ctx.author)
    if await usr.check_if_in_db():
      await ctx.reply("You already have an account bro.")
    else:
      await usr.create_account()
      await ctx.reply("Created a miner for you!", mention_author=False)

  
  @commands.command(name="deleteaccount")
  @check_if_in_db()
  async def deleteaccount(self,ctx):
    usr = user.User(ctx.author)
    cfmbtn = Button(label="CONFIRM", style=discord.ButtonStyle.danger)
    cfmview = view_timeout(timeout=10, ctx=ctx)
    cfmview.add_item(cfmbtn)
    await ctx.send("Are you ABSOLUTELY SURE you want to delete your account PERMANANTLY")
    msg = await ctx.send("This action CANNOT be undone", view=cfmview)
    cfmview.message = msg
    

    async def cfmcb(interaction):
      await usr.delete_user()
      cfmbtn.disabled = True
      await ctx.send("You deleted your account );")
      await interaction.response.edit_message(view=cfmview)

    cfmbtn.callback = cfmcb
      

def setup(bot: commands.bot):
  bot.add_cog(Miner(bot))