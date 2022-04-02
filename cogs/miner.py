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


  @commands.command(name="distribution", aliases=["dist"])
  async def distrubution(self, ctx):
    embed = discord.Embed(title="Miner Ore Distributing Chart", color=resource.random_color())
    embed.set_image(url="https://i.ibb.co/Rg90Qnn/b3bak5eige381-png.png")
    await ctx.send(embed=embed)
  
  @commands.command(name="mine", aliases=["dig"])
  async def mine(self, ctx):
    embed = discord.Embed(title=f"{ctx.author.name} goes mining!", color=resource.random_color())
    embed.add_field(name="current y-level", value=await user.get_user_data(ctx.author, "y"))
    minebtn = Button(label="Mine!", style=discord.ButtonStyle.primary, emoji="⛏")
    returnbtn = Button(label="Return to base", style=discord.ButtonStyle.primary, emoji="🏡")
    configbtn = Button(label="Mine settings", style=discord.ButtonStyle.primary, emoji="⚙")
    view = View()
    view.add_item(minebtn)
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
          await user.create_account(ctx.author)
          await ctx.send("Created a Miner for you!")
      else:
        await interaction.response.send_message("That's not your miner bro", ephemeral=True)

    async def returntobasecb(interaction):
      if interaction.user == ctx.author:
        if str(ctx.author.id) in db["users"]:
          if db["users"][str(ctx.author.id)]["y"] < 64:
            embed = discord.Embed(title="You Successfully returned to base!", color=discord.Colour.blurple())    
          else:
            await interaction.response.send_message("You are already in your base lol", ephemeral=True)
            embed.set_thumbnail(url="https://i.ibb.co/Zcvr3ps/3dfd7071185c7e046ecdbf2baa1fcb5b.jpg")
            
            minebtn.disabled = True         
            returnbtn.disabled = True
            configbtn.disabled = True
            await ctx.send(embed=embed)
            await interaction.response.edit_message(view=view)
            
        else:
          await user.create_account(ctx.author)
          await ctx.send("Created a Miner for you!")
      else:
        await interaction.response.send_message("That's not your miner bro", ephemeral=True)
        
    async def minecb(interaction):
      if interaction.user == ctx.author:
        if str(ctx.author.id) in db["users"]:
          await ctx.send("Working on it (:")
          minebtn.disabled = True
          returnbtn.disabled = True
          configbtn.disabled = True
          await interaction.response.edit_message(view=view)
        else:
          await user.create_account(ctx.author)
          await ctx.send("Created a Miner for you!")
      else:
        await interaction.response.send_message("That's not your miner bro", ephemeral=True)
           

    minebtn.callback = minecb
    returnbtn.callback = returntobasecb
    configbtn.callback = configcb
    
    

  @commands.command(name="info")
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
      await ctx.send(embed=embed)

def setup(bot: commands.bot):
  bot.add_cog(Miner(bot))