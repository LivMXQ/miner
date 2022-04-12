from discord.ext import commands

class Utility(commands.Cog):
  @commands.command(name="clear")
  @commands.has_permissions(manage_messages=True)
  async def clear(self, ctx, amount:int):
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)
    await ctx.channel.send(content=f"Successfully cleared {amount} messages from this channel",delete_after=5)

def setup(bot: commands.Bot):
  bot.add_cog(Utility(bot)) 