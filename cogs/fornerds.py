from discord.ext import commands
from replit import db
import user
import json


class ForNerds(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  @commands.is_owner()
  async def dump(self, ctx):
    try:
      with open("dump.json", "w") as f:
        json.dump(str(user.get_all_users()), f)
        await ctx.send("dumped!")
    except:
      await ctx.send("I THINK nothings in the db for now")
    

  @commands.command(name="update users",aliases=["uu"])
  @commands.is_owner()
  async def update_users(self, ctx):
    for i in db["users"]:
      user_ = user.User(user=await self.bot.fetch_user(int(i)))
      counter = user_.update_default_dict()
    await ctx.send(f"Successfully updated data for {counter} users")

  @commands.command()
  async def test(self, ctx, number):
    await ctx.send(user.calculate_level(int(number)))

def setup(bot: commands.bot):
  bot.add_cog(ForNerds(bot))

