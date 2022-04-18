import discord
import resource
import user
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

  def disable_all(self):
    for i in self.children:
      i.disabled = True


class Miner(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    initialize_cooldowns(cooldowns)
    self.item = resource.Item()
    self.currentview = None
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

  
  @commands.command(name="menu")
  @check_if_in_db()
  async def menu(self, ctx):
    usr = user.User(ctx.author)
  
    menuembed = discord.Embed(title=f"{ctx.author.name}'s miner menu")
    menuembed.add_field(name="current y-level", value=await usr.get_user_data("y"))
    menuembed.set_image(url="https://tryhardguides.com/wp-content/uploads/2022/03/featured-clash-royale-miner-update-768x432.jpg")
    rtbbtn = Button(label="Return to base", emoji="🏡")
    configbtn = Button(label="Miner Configurations", emoji="⚙")   
    endinteractionbtn = Button(label="End Interaction", row=1)
    
    menuview = view_timeout(ctx=ctx)
    self.currentview = menuview.setactive()
    menuview.add_item(configbtn)
    menuview.add_item(rtbbtn)
    menuview.add_item(endinteractionbtn)
    message = await ctx.reply(embed=menuembed, view=menuview, mention_author=False)
    menuview.message = message
    
    async def endinteractioncb(interaction):
      self.currentview.disable_all()
      await interaction.response.edit_message(view=self.currentview)
      
    endinteractionbtn.callback = endinteractioncb

    async def configbtncb(interaction):
        config = await usr.get_user_data("config")
        configembed = discord.Embed(title=f"{ctx.author.name}'s configurations menu")
        rtmbtn = Button(label="Go Back", emoji="🔙")
        configselect = Select() 
        for i in config:
          configselect.append_option(discord.SelectOption(label=i))
          configembed.add_field(name=i, value=config[i]) 
        configview = view_timeout(ctx=ctx)
        self.currentview = configview.setactive() 
        configview.add_item(configselect)
        configview.add_item(rtmbtn)
        endinteractionbtn.row = 2
        configview.add_item(endinteractionbtn)
        configview.message = message
        await interaction.response.edit_message(embed=configembed, view=configview)

        async def configselectcb(interaction):
          option = configselect.values[0]
          optionview = view_timeout(ctx)
          self.currentview = optionview.setactive()
          optionview.message = message
          if option == "Mining Direction":
            optionembed = discord.Embed(title=f"{ctx.author.name}'s configurations menu", description="Mining Direction")
            optionembed.add_field(name="Currently configured to", value=config["Mining Direction"])
            upbtn = Button(label="Mine Up!", emoji="⬆")
            downbtn = Button(label="Mine Down!", emoji="⬇")
            rtcbtn = Button(label="Go Back", emoji="🔙") 
            optionview.add_item(upbtn)
            optionview.add_item(downbtn)
            optionview.add_item(rtcbtn)
            optionview.add_item(endinteractionbtn)
            
            async def rtcbtncb(interaction):
              self.currentview = configview.setactive()
              await interaction.response.edit_message(embed=configembed, view=configview)
            
            async def upbtncb(interaction):
              
              await usr.update_user_data("config", "Mining Direction", "Up")
              config = await usr.get_user_data("config")
              optionembed.set_field_at(0, name="Currently configured to", value=config["Mining Direction"])  
              await interaction.response.edit_message(embed=optionembed, view=optionview)
              
            async def downbtncb(interaction):
              await usr.update_user_data("config", "Mining Direction", "Down")
              config = await usr.get_user_data("config")
              optionembed.set_field_at(0, name="Currently configured to", value=config["Mining Direction"])  
              await interaction.response.edit_message(embed=optionembed, view=optionview)

            rtcbtn.callback = rtcbtncb
            upbtn.callback = upbtncb
            downbtn.callback = downbtncb
            await interaction.response.edit_message(embed=optionembed, view=optionview)
              
          elif option == "Compact Mode":
            pass
          
        

        configselect.callback = configselectcb
        

        async def returntomenubtncb(interaction):
          self.currentview = menuview.setactive()
          await interaction.response.edit_message(embed=menuembed, view=menuview)

        rtmbtn.callback = returntomenubtncb

    
    async def returntobasecb(interaction):
      if await usr.returntobase():
        menuview.disable_all()
        await message.edit(view=menuview)
        await interaction.response.send_message("You Successfully returned to base!", ephemeral=True)                
      else:
        await interaction.response.send_message("You are already in your base lol", ephemeral=True)
   
      
    
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