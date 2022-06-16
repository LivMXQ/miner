from discord.ext import commands

class UserNotInDb(commands.CommandError):
  def __init__(self, user, message="User is not found in the database"):
    self.message = message
    super().__init__(self.message)

class Error(commands.Cog):  
  
  @commands.Cog.listener()
  async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.CommandNotFound):
      pass
      
    elif isinstance(error, commands.CommandOnCooldown): 
      message = f"This command is on cooldown. Try again after {int(error.retry_after)} seconds."
      await ctx.reply(content=message)
      
    elif isinstance(error, commands.MissingPermissions):
      message = "You don't have the permission for this!"
      await ctx.reply(content=message)
      
    elif isinstance(error, commands.UserInputError):
      message = "Invalid usage! Check your input and try again!"
      await ctx.reply(content=message)

    elif isinstance(error, commands.CheckFailure):
      message = "You are not supposed to do this!"
      await ctx.reply(content=message)

    elif isinstance(error, commands.NotOwner):
      message = "You are not the owner of the bot!"
      await ctx.reply(content=message)

    elif isinstance(error, UserNotInDb):
      message = "You do not have a Miner yet! Create a Miner using ;createaccount"
      await ctx.reply(content=message)
      
    else:
      message = f"!Something went wrong while running the command ):"
      print(error, type(error))
      await ctx.reply(content=message)

def setup(bot: commands.Bot):
  bot.add_cog(Error(bot))
