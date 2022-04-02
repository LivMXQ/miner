import discord
import json
from replit import db

async def get_cooldown(user):
  pass
async def get_drop_multipler():
  pass
  
async def create_account(user):
  db["users"][str(user.id)] = {"y":64, "inventory":{}, "pickaxe":["wooden_pickaxe", {}, 60]}
  role = discord.utils.get(user.guild.roles, name="minor")
  await user.add_roles(role)
  return True
 
async def update_user_data(user, type, value):
  if str(user.id) in db["users"]:
    db["users"][str(user.id)][type] = value
    return True
  else:
    return False
  
async def get_user_data(user, type):
  if str(user.id) in db["users"]:
    value = db["users"][str(user.id)][type]
    return value
  else:
    return None
  
  
    


    
