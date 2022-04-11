import user
import discord
from discord.ext import commands


class ForNerds(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="modifyuser", aliases=["mdfu"])
  @commands.is_owner()
  async def modifyuser(self, ctx, member:discord.User, type, *value):
    usr = user.User(member)
    if len(value) == 1:
      await usr.update_user_data(type, value[0])
      await ctx.send("Successful!")
               
    elif len(value) == 2:
      await usr.update_user_data(type, value[0], value[1])
      await ctx.send("Successful!")

  @commands.command(name="getallusers", aliases=["gau", "fuckingrandomshit","frs"])
  @commands.is_owner()
  async def getallusers(self, ctx):
    dict = user.get_all_users()
    stripdict = {}
    for a in dict:
      stripdict[a] = dict[a]
    await ctx.send(stripdict)
    
    
     

def setup(bot: commands.bot):
  bot.add_cog(ForNerds(bot))

