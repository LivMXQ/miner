import discord
import resource
import user
import random
from replit import db
from discord.ext import commands
from discord.ui import Button, Select, View

def initialize_cooldowns():  # This function still needs to be called somewhere.
    for i in db["users"]:
      user_id = i
      duration = 17.5
      cooldowns[user_id] = commands.CooldownMapping.from_cooldown(1, duration, commands.BucketType.user)

class view_timeout(View):
  def __init__(self, timeout, ctx):
    super().__init__(timeout=timeout)
    self.inactive = False
    self.ctx = ctx
   
  async def on_timeout(self):
    if self.inactive == False:
      for i in self.children:
        child = i
        child.disabled=True
      
      await self.message.edit(view=self)


  async def interaction_check(self, interaction: discord.Interaction):
    if interaction.user != self.ctx.author:
      await interaction.response.send_message("That's not your miner bro", ephemeral=True)
      return False
    else:
      return True


class Miner(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    global cooldowns 
    cooldowns = dict()
    initialize_cooldowns()
    self.item = resource.Item()
    self.allitems = self.item.getallitems()


  def check_cooldown():
    async def predicate(ctx):
      user_id = str(ctx.author.id)
      if user_id == "789359497894035456":
        return True
      else:
        if cooldowns and user_id in cooldowns:
          bucket = cooldowns[user_id].get_bucket(ctx.message)
          retry_after = bucket.update_rate_limit()
          if retry_after:
            raise commands.CommandOnCooldown(bucket, retry_after, commands.BucketType.user)
          return True
        else:
          usr = user.User(ctx.author)
          await usr.create_account()
          await ctx.send("Created a minor for you!")
          return True
    return commands.check(predicate)


  async def minefn(self, ctx):
    usr = user.User(ctx.author)
    loot = "".join(await resource.mine_loot(await usr.get_user_data("y")))
    if loot == "event":
      embed = discord.Embed(title=f"{ctx.author.name}'s event", color=discord.Colour.gold())
           
    else:
      multipler = await usr.get_multipler()
      config = await usr.get_user_data("config")
      if config["direction"] == "down" and await usr.get_user_data("y")>=-60:
        await usr.update_user_data("y", await usr.get_user_data("y") - random.randrange(0,5))
      elif config["direction"] == "down" and await usr.get_user_data("y")==-61:
        await usr.update_user_data("y", await usr.get_user_data("y") - random.randrange(0,4))
      elif config["direction"] == "down" and await usr.get_user_data("y")==-62:
        await usr.update_user_data("y", await usr.get_user_data("y") - random.randrange(0,3))
      elif config["direction"] == "down" and await usr.get_user_data("y")==-63:
        await usr.update_user_data("y", await usr.get_user_data("y") - random.randrange(0,2))
      elif config["direction"] == "up" and await usr.get_user_data("y")<=60:
        await usr.update_user_data("y", await usr.get_user_data("y") + random.randrange(0,5))
      elif config["direction"] == "down" and await usr.get_user_data("y")==61:
        await usr.update_user_data("y", await usr.get_user_data("y") + random.randrange(0,4))
      elif config["direction"] == "down" and await usr.get_user_data("y")==62:
        await usr.update_user_data("y", await usr.get_user_data("y") + random.randrange(0,3))
      elif config["direction"] == "down" and await usr.get_user_data("y")==63:
        await usr.update_user_data("y", await usr.get_user_data("y") + random.randrange(0,2))
      embed = discord.Embed(title=f"{ctx.author.name}'s booty", colour=resource.uncommon())
      embed.set_thumbnail(url="https://i.ibb.co/f8Lsxkb/Small-Mining-Sack.jpg")
      name = self.allitems[loot]["name"]
      id = self.allitems[loot]["id"]
      embed.add_field(value=f"You swung your pickaxe and got {multipler} {name} {id}", name='\u200b')
      y = await usr.get_user_data("y")
      embed.set_footer(text=f"new y-level ─  {y}")
      

      inventory = user.Inventory(ctx.author)
      await inventory.add_item(loot, multipler)
    return embed
    

    
  @commands.command(name="distribution", aliases=["dist"])
  async def distrubution(self, ctx):
    embed = discord.Embed(title="Miner Ore Distributing Chart", color=discord.Colour.random())
    embed.set_image(url="https://i.ibb.co/Rg90Qnn/b3bak5eige381-png.png")
    await ctx.send(embed=embed)


  
  @commands.command(name="mine", aliases=["dig"])
  @check_cooldown()
  async def mine(self, ctx):
    usr = user.User(ctx.author)
    if str(ctx.author.id) in db["users"]:
      embed = await self.minefn(ctx)
      await ctx.send(embed=embed) 
 
    else:
      await usr.create_account()
      await ctx.send("Created a Miner for you!")

  async def menufn(self, ctx):
    usr = user.User(ctx.author)
    embed = discord.Embed(title=f"{ctx.author.name}'s miner menu", color=discord.Colour.random())
    embed.add_field(name="current y-level", value=await usr.get_user_data("y"))
    embed.set_image(url="https://tryhardguides.com/wp-content/uploads/2022/03/featured-clash-royale-miner-update-768x432.jpg")
    
    return embed
  
  @commands.command(name="menu")
  async def menu(self, ctx):
    usr = user.User(ctx.author)
    if str(ctx.author.id) in db["users"]:
      menuembed = await self.menufn(ctx)
      rtbbtn = Button(label="Return to base", style=discord.ButtonStyle.primary, emoji="🏡")
      configbtn = Button(label="Mine settings", style=discord.ButtonStyle.primary, emoji="⚙")
      configembed = discord.Embed(title=f"{ctx.author.name}'s configurations menu")
      config = await usr.get_user_data("config")
      print(config)
      configselect = Select(options=[
        discord.SelectOption(label="direction")
      ])
      rtmbtn = Button(label="Go back", style=discord.ButtonStyle.primary, emoji="🔙")
      menuview = view_timeout(timeout=10, ctx=ctx)
      configview = view_timeout(timeout=10, ctx=ctx)
      menuview.add_item(configbtn)
      menuview.add_item(rtbbtn)
      configview.add_item(configselect)
      configview.add_item(rtmbtn)
      menumessage = await ctx.send(embed=menuembed, view=menuview)
      menuview.message = menumessage
      configview.message = menumessage
    else:
      await usr.create_account()
      await ctx.send("Created a Miner for you!")


    async def configcb(interaction):
      if await menuview.interaction_check(interaction=interaction):
        menuview.inactive = True
        configview.inactive = False     
        await interaction.response.edit_message(embed=configembed, view=configview)
      else:
        await interaction.response.send_message("That's not your miner bro", ephemeral=True)

      async def returntomenucb(interaction):
        configview.inactive = True
        menuview.inactive = False
        await interaction.response.edit_message(embed=menuembed, view=menuview)

      rtmbtn.callback = returntomenucb

    
    async def returntobasecb(interaction):
      if menuview.interaction_check(interaction=interaction):
        if await usr.returntobase():
          embed = discord.Embed(title="You Successfully returned to base!", color=discord.Colour.green())
          embed.set_thumbnail(url="https://i.ibb.co/Zcvr3ps/3dfd7071185c7e046ecdbf2baa1fcb5b.jpg")
          embed.add_field(name="New y-level", value=await usr.get_user_data("y"))
          await ctx.send(embed=embed)       
          rtbbtn.disabled = True
          configbtn.disabled = True
            
          await interaction.response.edit_message(view=menuview)

        else:
          await interaction.response.send_message("You are already in your base lol", ephemeral=True)
      else:
        await interaction.response.send_message("That's not your miner bro", ephemeral=True)

  
    rtbbtn.callback = returntobasecb
    configbtn.callback = configcb

  @commands.command(name="createaccount", aliases=["start", "create"])
  async def createaccount(self, ctx):
    usr = user.User(ctx.author)
    await usr.create_account()
    await ctx.send("Created a miner for you!")
    
  @commands.command(name="inventory",aliases=["inv"])
  async def inventory(self, ctx):  
    usr = user.User(ctx.author)
    if str(ctx.author.id) in db["users"]:  
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
    else:
      await usr.create_account()
      await ctx.send("Created a Miner for you!")

  
  @commands.command(name="deleteaccount")
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