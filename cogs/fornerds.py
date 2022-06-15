from discord.ext import commands


class ForNerds(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
        

def setup(bot: commands.bot):
  bot.add_cog(ForNerds(bot))

