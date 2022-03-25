import discord
import resource
import user
import random
from discord.ext import commands
from discord.ui import Button, View


class Miner(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  async def minerng(self):
    event = random.choices(resource.lootable.keys())
    
  @commands.command(name="distribution", aliases=["dist"])
  async def distrubution(self, ctx):
    embed = discord.Embed(title="Miner Ore Distributing Chart")
    embed.set_image(url="https://i.ibb.co/Rg90Qnn/b3bak5eige381-png.png")
    await ctx.send(embed=embed)
  
  @commands.command(name="mine", aliases=["dig"])
  async def mine(self, ctx):
    embed = discord.Embed(title=f"{ctx.author.name} goes mining!")
    attackbtn = Button(label="Attack", style=discord.ButtonStyle.primary, emoji="💥")
    talkbtn = Button(label="Talk", style=discord.ButtonStyle.primary, emoji="👶")
    view = View()
    view.add_item(attackbtn)
    view.add_item(talkbtn)
    await ctx.send(embed=embed, view=view)    

    
    '''users = await user.get_users()
    allitems = resource.get_all_items()
    if str(ctx.author.id) in users:
      loot = "".join(await resource.mine(await user.get_user_data(ctx.author, "y")))
      embed = discord.Embed(title=f"{ctx.author.name}'s booty")
      embed.add_field(value=loot, name=allitems[loot])
      embed.set_footer(text="Items are NOT added to inv YET")
      await ctx.send(embed=embed)
    else:
      await user.create_account(ctx.author)
      await ctx.send("Created a Miner account for you!")'''
    

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