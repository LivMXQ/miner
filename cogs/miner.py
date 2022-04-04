import discord
import resource
import user
import random
from replit import db
from discord.ext import commands
from discord.ui import Button, View


class Miner(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  async def minefn(self, ctx):
    usr = user.User(ctx.author)
    loot = "".join(await resource.mine_loot(await usr.get_user_data("y")))
    if loot == "event":
      embed = discord.Embed(title=f"{ctx.author.name}'s event", color=discord.Colour.gold())
           
    else:
      multipler = await usr.get_multipler()
      config = await usr.get_user_data("config")
      if config["direction"] == "down" and await usr.get_user_data("y") >= -60:
        await usr.update_user_data("y", await usr.get_user_data("y") - random.randrange(0,5))
      elif config["direction"] == "up" and await usr.get_user_data("y")<=60:
        await usr.update_user_data("y", await usr.get_user_data("y") + random.randrange(0,5))
      embed = discord.Embed(title=f"{ctx.author.name}'s booty", colour=resource.uncommon())
      embed.set_thumbnail(url="https://i.ibb.co/f8Lsxkb/Small-Mining-Sack.jpg")
      embed.add_field(name=resource.allitems[loot]["id"], value=f"{multipler} x {loot}")
      y = await usr.get_user_data("y")
      embed.set_footer(text=f"new y-level ─ {y}")
      

      inventory = user.Inventory(ctx.author)
      await inventory.add_item(loot, multipler)
    return embed
   
    

    
  @commands.command(name="distribution", aliases=["dist"])
  async def distrubution(self, ctx):
    embed = discord.Embed(title="Miner Ore Distributing Chart", color=discord.Colour.random())
    embed.set_image(url="https://i.ibb.co/Rg90Qnn/b3bak5eige381-png.png")
    await ctx.send(embed=embed)

  @commands.command(name="mine", aliases=["dig"])
  async def mine(self, ctx):
    if str(ctx.author.id) in db["users"]:
      embed = await self.minefn(ctx)
      await ctx.send(embed=embed) 
 
    else:
      await usr.create_account()
      await ctx.send("Created a Miner for you!")

  
  
  @commands.command(name="menu")
  async def menu(self, ctx):
    usr = user.User(ctx.author)
    embed = discord.Embed(title=f"{ctx.author.name} goes mining!", color=discord.Colour.random())
    embed.add_field(name="current y-level", value=await usr.get_user_data("y"))
    embed.set_image(url="https://tryhardguides.com/wp-content/uploads/2022/03/featured-clash-royale-miner-update-768x432.jpg")
    returnbtn = Button(label="Return to base", style=discord.ButtonStyle.primary, emoji="🏡")
    configbtn = Button(label="Mine settings", style=discord.ButtonStyle.primary, emoji="⚙")
    view = View()
    view.add_item(configbtn)
    view.add_item(returnbtn)
    await ctx.send(embed=embed, view=view)   


    async def configcb(interaction):
      if interaction.user == ctx.author:
        if str(ctx.author.id) in db["users"]:
          await ctx.send("Working on it (:")
          minebtn.disabled = True
          returnbtn.disabled = True
          configbtn.disabled = True
          await interaction.response.edit_message(view=view)
        else:
          await usr.create_account()
          await ctx.send("Created a Miner for you!")
      else:
        await interaction.response.send_message("That's not your miner bro", ephemeral=True)

    async def returntobasecb(interaction):
      if interaction.user == ctx.author:
        if str(ctx.author.id) in db["users"]:
          if await usr.returntobase():
            embed = discord.Embed(title="You Successfully returned to base!", color=discord.Colour.green())
            
            embed.set_thumbnail(url="https://i.ibb.co/Zcvr3ps/3dfd7071185c7e046ecdbf2baa1fcb5b.jpg")
            embed.add_field(name="New y-level", value=await usr.get_user_data("y"))
            await ctx.send(embed=embed)
            minebtn.disabled = True         
            returnbtn.disabled = True
            configbtn.disabled = True
            
            await interaction.response.edit_message(view=view)

          else:
            await interaction.response.send_message("You are already in your base lol", ephemeral=True)
                      
        else:
          await usr.create_account()
          await interaction.response.send_message("Created a Miner for you!")
      else:
        await interaction.response.send_message("That's not your miner bro", ephemeral=True)

  
    returnbtn.callback = returntobasecb
    configbtn.callback = configcb
    
  @commands.command(name="inventory",aliases=["inv"])
  async def inventory(self, ctx):  
    usr = user.User(ctx.author)
    embed = discord.Embed(title=f"{ctx.author.name}'s inventory", color=discord.Colour.random())
    invdict = await usr.get_user_data("inventory")
    for i in invdict:
      embed.add_field(name=f"{i} ─ {invdict[i]}", value=None, inline=False)
    embed.set_footer(text="yes")
    await ctx.send(embed=embed)

  """@commands.command(name="info")
  async def info(self, ctx, *args):
    if args:
      await ctx.send("Not a thing yet lol")
    else:
      embed = discord.Embed(title="Info", description="List of items", color=resource.random_color())
      itemlist = []
      for key in resource.category:
        dict = resource.category[key]
        for key1 in dict:
          itemlist.append(dict[key1])
        embed.add_field(name=key, value="".join(itemlist), inline=False)
        itemlist = []
      
      embed.set_footer(text=";info <Item_Id> for more details")
      await ctx.send(embed=embed)"""

def setup(bot: commands.bot):
  bot.add_cog(Miner(bot))