import discord
import resource
import time
from discord.ext import commands


class MyHelp(commands.HelpCommand):  
  def __init__(self):
    super().__init__(command_attrs={'help': 'Shows help about the bot, a command, or a category'})

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
    embed = discord.Embed(title=f"-{command} info", color=resource.random_color())
    embed.add_field(name="Description", value=command.help)
    embed.add_field(name='Usage', value=self.get_command_signature(command), inline=False)
    try:
      cooldown = command.cooldown.per / command.cooldown.rate
      embed.add_field(name='Cooldown', value=f'{cooldown}s')
    except:
      pass
    alias = ", -".join(command.aliases)
    if alias:
      embed.add_field(name="Aliases", value=f"-{alias}", inline=False)
    embed.set_footer(text="Usage Syntax: <required> [optional]")

    channel = self.get_destination()
    await channel.send(embed=embed)

    
  async def send_bot_help(self, mapping):
    channel = self.get_destination()
    embed = discord.Embed(title="Help", color=resource.random_color())
    for cog, commands in mapping.items():
      filtered = await self.filter_commands(commands, sort=True)
      command_signatures = [self.get_command_signature(c) for c in filtered]
      if command_signatures:
        cog_name = getattr(cog, "qualified_name", "No Category")
        embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)
    await channel.send(embed=embed)


  async def send_error_message(self, error):
    embed = discord.Embed(title="Error", description=error, color=discord.Colour.red())
    channel = self.get_destination()
    await channel.send(embed=embed)
    time.sleep(5)
    await channel.purge(limit=2)
    

class Help(commands.Cog):
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = MyHelp()
        bot.help_command.cog = self
        
    def cog_unload(self):
        self.bot.help_command = self._original_help_command


def setup(bot: commands.bot):
  bot.add_cog(Help(bot))

