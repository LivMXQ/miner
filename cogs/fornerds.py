from discord.ext import commands
from replit import db
import user


class ForNerds(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def frs(self, ctx):
    await ctx.send(user.get_all_users())

  @commands.command(aliases=["uu"])
  async def update_users(self, ctx):

    for i in db["users"]:
      user_ = user.User(self.bot.get_user(int(i)))
      counter = user_.update_default_dict()
    await ctx.send(f"Successfully updated data for {counter} users")

def setup(bot: commands.bot):
  bot.add_cog(ForNerds(bot))

