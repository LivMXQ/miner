import discord
import os
from discord.ext import commands

bot_colour = int(os.getenv("COLOUR"))

class MyHelp(commands.HelpCommand):  
  def __init__(self):
    super().__init__(command_attrs={'help': 'Shows help about the bot, a command, or a category'})

  def get_destination(self):
    return self.context

  def get_command_signature(self, command):
    if "=" in command.signature:
      siglist = command.signature.split(" ")
      striplist = []
      for i in range(0,len(siglist)):
        fullstring = siglist[i].split("=")[0] + "]"
        striplist.append(fullstring)
      clean_signature = " ".join(striplist)
    
      return f'{self.context.clean_prefix}{command} {clean_signature}'
    else:
      return f'{self.context.clean_prefix}{command} {command.signature}'
      
    
  async def send_command_help(self, command):
    embed = discord.Embed(title=os.getenv("PREFIX") + command.name + " info", color=bot_colour)
    embed.add_field(name="Description", value=command.help)
    embed.add_field(name='Usage', value=self.get_command_signature(command), inline=False)
    try:
      cooldown = command.cooldown.per / command.cooldown.rate
      embed.add_field(name='Cooldown', value=f'{cooldown}s')
    except:
      pass
    alias = (", "+os.getenv("PREFIX")).join(command.aliases)
    if alias:
      embed.add_field(name="Aliases", value=os.getenv("PREFIX")+alias, inline=False)
    embed.set_footer(text="Usage Syntax: <required> [optional]")

    ctx = self.get_destination()
    await ctx.send(embed=embed)

    
  async def send_bot_help(self, mapping):
    ctx = self.get_destination()
    embed = discord.Embed(title="Minor 2.0 List of Commands", color=bot_colour)
    for cog, command in mapping.items():
      filtered = await self.filter_commands(command, sort=True)
      command_signatures = [self.get_command_signature(c) for c in filtered]
      if command_signatures:
        cog_name = getattr(cog, "qualified_name", "No Category")
        embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)
    await ctx.send(embed=embed)


  async def send_error_message(self, error):
    embed = discord.Embed(title="Error", description=error, color=discord.Colour.red())
    ctx = self.get_destination()
    await ctx.send(embed=embed)

    

class Help(commands.Cog):
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = MyHelp()
        bot.help_command.cog = self
        
    def cog_unload(self):
        self.bot.help_command = self._original_help_command


def setup(bot: commands.bot):
  bot.add_cog(Help(bot))

