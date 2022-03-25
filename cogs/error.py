import time
from discord.ext import commands

class Error(commands.Cog):  
  
  @commands.Cog.listener()
  async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.CommandNotFound):
      message = f"The command you used is not found ):"
      await ctx.send(content=message)
      time.sleep(5)
      await ctx.channel.purge(limit=2)
      
    elif isinstance(error, commands.CommandOnCooldown):
      message = f"This command is on cooldown. Try again after {round(error.retry_after, 1)} seconds."
      await ctx.send(content=message)
      time.sleep(5)
      await ctx.channel.purge(limit=2)
      
    elif isinstance(error, commands.MissingPermissions):
      message = "You don't have the permission for this!"
      await ctx.send(content=message)
      time.sleep(5)
      await ctx.channel.purge(limit=2)
      
    elif isinstance(error, commands.UserInputError):
      message = "Invalid usage! Check your input and try again!"
      await ctx.send(content=message)
      time.sleep(5)
      await ctx.channel.purge(limit=2)

    elif isinstance(error, commands.CheckFailure):
      message = "You are not supposed to do this!"
      await ctx.send(content=message)
      time.sleep(5)
      await ctx.channel.purge(limit=2)

    elif isinstance(error, commands.NotOwner):
      message = "You are not the owner of the bot!"
      await ctx.send(content=message)
      time.sleep(5)
      await ctx.channel.purge(limit=2)
      
    else:
      await ctx.message.delete(delay=5)
      message = f"! Something went wrong while running the command! {error}"
      await ctx.send(content=message)
      time.sleep(5)
      await ctx.channel.purge(limit=2)
  

def setup(bot: commands.Bot):
  bot.add_cog(Error(bot))
