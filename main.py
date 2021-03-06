import os
import discord
from discord.ext import commands
from keep_alive import keep_alive
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix=os.getenv("PREFIX"), case_insensitive=True, intents=discord.Intents.all())


for filename in os.listdir('./cogs'):
  if filename.endswith('.py') and filename != "__init__.py":    
    bot.load_extension(f'cogs.{filename[:-3]}', store=False)


@bot.event
async def on_ready():
  await bot.change_presence(activity = discord.Activity(type=discord.ActivityType.listening, name=os.getenv("PREFIX")+"help"), status=discord.Status.online)
  print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_disconnect():
    print("bot disconnected")


@bot.event
async def on_connect():
    print("bot connected")
  

try:
  keep_alive()
  bot.run(os.getenv('TOKEN'))
except:
  os.system("kill 1")

