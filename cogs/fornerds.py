import user
import discord
from discord.ext import commands


class ForNerds(commands.Cog):
  def __init__(self, bot):
    self.bot = bot


  @commands.command(name="getallusers", aliases=["gau", "fuckingrandomshit","frs"])
  @commands.is_owner()
  async def getallusers(self, ctx):
    dict = user.get_all_users()
    print(dict)
    
    
     

def setup(bot: commands.bot):
  bot.add_cog(ForNerds(bot))

