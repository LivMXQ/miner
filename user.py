import discord
import json


  
async def create_account(user):
  users = await get_users()
  if str(user.id) in users:
    return False
  else:
    users[str(user.id)] = {}
    users[str(user.id)]["pickaxe"] = ["Wooden_Pickaxe", [None]]
    users[str(user.id)]["y"] = 64
    users[str(user.id)]["inventory"] = []
    
    with open("user.json", "w") as f:
      json.dump(users,f)
      return True
 
async def get_user_data(user, type):
  users = await get_users()
  if str(user.id) not in users:
    return False
  else:
    value = users[str(user.id)][type]
    return value
    
  
async def get_users():
  with open("user.json", "r") as f:
    users = json.load(f)

  return users