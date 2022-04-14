import discord
import resource
import user
import random
from replit import db
from cogs.error import UserNotInDb
from discord.ext import commands
from discord.ui import Button, Select, View

cooldowns = dict()
registeredviews = list()

def initialize_cooldowns(kooldowns):
  for i in db["users"]:
    user_id = i
    duration = 17.5
    kooldowns[user_id] = commands.CooldownMapping.from_cooldown(1, duration, commands.BucketType.user)


class view_timeout(View):
  def __init__(self, ctx, timeout=20):
    super().__init__(timeout=timeout)
    self.register()
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

  def register(self):
    registeredviews.append(self)

  def setactive(self):
    for i in registeredviews:
      i.inactive = True
    self.inactive = False

  def disable_all(self):
    for i in self.children:
      i.disabled = True


class Miner(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    initialize_cooldowns(cooldowns)
    self.item = resource.Item()
    self.allitems = self.item.getallitems()


  def check_cooldown():
    async def predicate(ctx):
      user_id = str(ctx.author.id)
      if user_id == "789359497894035456":
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


  async def minefn(self, ctx):
    usr = user.User(ctx.author)
    loot = "".join(await resource.mine_loot(await usr.get_user_data("y")))
    if loot == "event":
      embed = discord.Embed(title=f"{ctx.author.name}'s event", color=discord.Colour.gold())
           
    else:
      multipler = await usr.get_multipler()
      config = await usr.get_user_data("config")
      if config["Mining Direction"] == "Down" and await usr.get_user_data("y")>=-60:
        await usr.update_user_data("y", await usr.get_user_data("y") - random.randrange(0,5))
      elif config["Mining Direction"] == "Down" and await usr.get_user_data("y")==-61:
        await usr.update_user_data("y", await usr.get_user_data("y") - random.randrange(0,4))
      elif config["Mining Direction"] == "Down" and await usr.get_user_data("y")==-62:
        await usr.update_user_data("y", await usr.get_user_data("y") - random.randrange(0,3))
      elif config["Mining Direction"] == "Down" and await usr.get_user_data("y")==-63:
        await usr.update_user_data("y", await usr.get_user_data("y") - random.randrange(0,2))
      elif config["Mining Direction"] == "Up" and await usr.get_user_data("y")<=60:
        await usr.update_user_data("y", await usr.get_user_data("y") + random.randrange(0,5))
      elif config["Mining Direction"] == "Up" and await usr.get_user_data("y")==61:
        await usr.update_user_data("y", await usr.get_user_data("y") + random.randrange(0,4))
      elif config["Mining Direction"] == "Up" and await usr.get_user_data("y")==62:
        await usr.update_user_data("y", await usr.get_user_data("y") + random.randrange(0,3))
      elif config["Mining Direction"] == "Up" and await usr.get_user_data("y")==63:
        await usr.update_user_data("y", await usr.get_user_data("y") + random.randrange(0,2))
      
      name = self.allitems[loot]["name"]
      id = self.allitems[loot]["id"]
      rarity = self.allitems[loot]["rarity"]
      embed = discord.Embed(title=f"{ctx.author.name}'s booty", colour=resource.uncommon())
      embed.set_thumbnail(url="https://i.ibb.co/f8Lsxkb/Small-Mining-Sack.jpg")
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
    await ctx.reply(embed=embed, mention_author=False)


  
  @commands.command(name="mine", aliases=["dig"])
  @check_cooldown()
  @check_if_in_db()
  async def mine(self, ctx):
    embed = await self.minefn(ctx)
    await ctx.reply(embed=embed, mention_author=False) 


  async def menufn(self, ctx):
    usr = user.User(ctx.author)
    embed = discord.Embed(title=f"{ctx.author.name}'s miner menu", color=discord.Colour.random())
    embed.add_field(name="current y-level", value=await usr.get_user_data("y"))
    embed.set_image(url="https://tryhardguides.com/wp-content/uploads/2022/03/featured-clash-royale-miner-update-768x432.jpg")
    
    return embed
  
  @commands.command(name="menu")
  @check_if_in_db()
  async def menu(self, ctx):
    usr = user.User(ctx.author)
  
    menuembed = await self.menufn(ctx)
    rtbbtn = Button(label="Return to base", style=discord.ButtonStyle.primary, emoji="🏡")
    configbtn = Button(label="Miner Configurations", style=discord.ButtonStyle.primary, emoji="⚙")    
       
    menuview = view_timeout(timeout=10, ctx=ctx)
    configview = view_timeout(timeout=10, ctx=ctx)
    menuview.add_item(configbtn)
    menuview.add_item(rtbbtn)
       
    menumessage = await ctx.reply(embed=menuembed, view=menuview, mention_author=False)
    menuview.message = menumessage
    

    async def configbtncb(interaction):
      if await menuview.interaction_check(interaction=interaction):
        config = await usr.get_user_data("config")
        print(config)
        configembed = discord.Embed(title=f"{ctx.author.name}'s configurations menu")
        rtmbtn = Button(label="Go Back", style=discord.ButtonStyle.primary, emoji="🔙")
        configselect = Select() 
        configview.add_item(configselect)
        configview.add_item(rtmbtn)
        configview.message = menumessage
        for i in config:
          configselect.append_option(discord.SelectOption(label=i))
          configembed.add_field(name=i, value=config[i])        
        configview.setactive() 
        await interaction.response.edit_message(embed=configembed, view=configview)
      else:
        await interaction.response.send_message("That's not your miner bro", ephemeral=True)

        async def configselectcb(interaction):
          option = configselect.values[0]
          if option == "Mining Direction":
            optionembed = discord.Embed(title=f"{ctx.author.name}'s configurations menu", description="Mining Direction")
            optionembed.add_field(name="Currently configured to", value=config["Mining Direction"])
            upbtn = Button(label="Mine Up!", emoji="⬆")
            downbtn = Button(lable="Mine Down!", emoji="⬇")
            optionview = view_timeout(ctx)
            optionview.add_item(upbtn)
            optionview.add_item(downbtn)
          elif option == "Compact Mode":
            pass
          optionview.message = await interaction.response.edit_message(embed=optionembed, view=optionview)

        configselect.callback = configselectcb

      

        async def returntomenubtncb(interaction):
          configview.setactive()
          await interaction.response.edit_message(embed=menuembed, view=menuview)

        rtmbtn.callback = returntomenubtncb

    
    async def returntobasecb(interaction):
      if await menuview.interaction_check(interaction=interaction):
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
    configbtn.callback = configbtncb

    
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