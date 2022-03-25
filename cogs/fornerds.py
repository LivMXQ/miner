import discord
import resource
import time
from discord.ext import commands


class ForNerds(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="test")
  @commands.is_owner()
  async def test(self, ctx):
    await ctx.message.delete()
    await ctx.send("Fuck privilaged intents im back baby")
    

  @commands.command(name="resourcestest", aliases=["rct"])
  @commands.is_owner()
  async def resourcestest(self, ctx):
    await ctx.send(resource.allitemdict)

  @commands.command(name="emojitest", aliases=["ejt"])
  @commands.is_owner()
  async def emojitest(self, ctx, item):
    if item in resource.allitemdict:
      await ctx.send(resource.allitemdict[item])
    else:
      await ctx.send(content="invalid input!")
      time.sleep(5)
      await ctx.channel.purge(limit=2)
    

  @commands.command(name="embedtest", aliases=["ebt"])
  @commands.is_owner()
  async def embedtest(self, ctx, item):
    if item in resource.allitemdict:
      embed = discord.Embed()
      embed.add_field(name=item, value=resource.allitemdict[item])
      await ctx.send(embed=embed)
    else:
      await ctx.send(content="invalid input!")
      time.sleep(5)
      await ctx.channel.purge(limit=2)
     
    

def setup(bot: commands.bot):
  bot.add_cog(ForNerds(bot))

