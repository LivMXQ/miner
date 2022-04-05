import discord
from replit import db

class Inventory:
  def __init__(self, user):
    self.user = user
    self.dict = db["users"][str(user.id)]["inventory"]

  async def add_item(self, item, amount):
    if item not in self.dict:
      self.dict[item] = amount
    else:     
      self.dict[item] += amount
    for i in self.dict:
      db["users"][str(self.user.id)]["inventory"][i] = self.dict[i]

  async def remove_item(self, item, amount):
    if item not in self.dict:
      return False
    else:     
      self.dict[item] -= amount
    for i in self.dict:
      db["users"][str(self.user.id)]["inventory"][i] = self.dict[i]


class User:
  def __init__(self, user):
    self.user = user

  
  async def get_cooldown(self):
    return 20


  async def get_multipler(self):
    return 1

  async def returntobase(self):
    if db["users"][str(self.user.id)]["y"] < 64:
      db["users"][str(self.user.id)]["y"] = 64
      return True
    else:
      return False
      
  async def create_account(self):
    db["users"][str(self.user.id)] = {"y":64, "inventory":{}, "pickaxe":["wooden_pickaxe", {}, 60]}
    role = discord.utils.get(self.user.guild.roles, name="minor")
    await self.user.add_roles(role)
    return True
    
  async def update_user_data(self, type, value):
    if str(self.user.id) in db["users"]:
      db["users"][str(self.user.id)][type] = value
      return True
    else:
      return False
  
  async def get_user_data(self, type):
    if str(self.user.id) in db["users"]:
      value = db["users"][str(self.user.id)][type]
      return value
    else:
      return None
  
  
    


    
