import discord
import resource
from discord.ext import commands


class ForNerds(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="test")
  @commands.is_owner()
  async def test(self, ctx):
    await ctx.message.delete()
    await ctx.send("Fuck privilaged intents im back baby")
     

def setup(bot: commands.bot):
  bot.add_cog(ForNerds(bot))

