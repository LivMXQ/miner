import discord
import random
import cogs.miner as miner


def get_all_users():
  return db["users"]

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


class User: #all here
  def __init__(self, user):
    self.user = user

  
  async def get_cooldown(self): #still working on this 
    return 17


  async def get_multipler(self): #still working on this
    return 1

  async def returntobase(self):
    if db["users"][str(self.user.id)]["y"] < 64:
      db["users"][str(self.user.id)]["y"] = 64
      return True
    else:
      return False
      
  async def create_account(self):
    db["users"][str(self.user.id)] = {'y': 64, 'inventory': {}, 'pickaxe': ['wooden_pickaxe', {}, 60], 'config': {'Mining Direction': 'down'}, "story":0}
    miner.initialize_cooldowns(miner.cooldowns)
    if isinstance(self.user, discord.Member):
      try:
        role = discord.utils.get(self.user.guild.roles, name="Minor ⛏️")
        await self.user.add_roles(role)
      except:
        print("WARN: Minor role not granted on account create")
    return True
    
  async def update_user_data(self, type, *value):
    if await self.check_if_in_db():
      if len(value) == 1:
        db["users"][str(self.user.id)][type] = value[0]
        return True
               
      elif len(value) == 2:
        db["users"][str(self.user.id)][type][value[0]] = value[1]
        return True
    else:
      return False
    
  async def get_user_data(self, type):
    if await self.check_if_in_db():
      value = db["users"][str(self.user.id)][type]
      return value
    else:
      return False

  async def check_if_in_db(self):
    if str(self.user.id) in db["users"]:
      return True
    else:
      return False

  async def delete_user(self):
    db["users"].pop(str(self.user.id))
    return True

  async def change_y(self):
    config = await self.get_user_data("config")
    if config["Mining Direction"] == "Down" and await self.get_user_data("y")>=-60:
      await self.update_user_data("y", await self.get_user_data("y") - random.randrange(0,5))
    elif config["Mining Direction"] == "Down" and await self.get_user_data("y")==-61:
      await self.update_user_data("y", await self.get_user_data("y") - random.randrange(0,4))
    elif config["Mining Direction"] == "Down" and await self.get_user_data("y")==-62:
      await self.update_user_data("y", await self.get_user_data("y") - random.randrange(0,3))
    elif config["Mining Direction"] == "Down" and await self.get_user_data("y")==-63:
      await self.update_user_data("y", await self.get_user_data("y") - random.randrange(0,2))
    elif config["Mining Direction"] == "Up" and await self.get_user_data("y")<=60:
      await self.update_user_data("y", await self.get_user_data("y") + random.randrange(0,5))
    elif config["Mining Direction"] == "Up" and await self.get_user_data("y")==61:
      await self.update_user_data("y", await self.get_user_data("y") + random.randrange(0,4))
    elif config["Mining Direction"] == "Up" and await self.get_user_data("y")==62:
      await self.update_user_data("y", await self.get_user_data("y") + random.randrange(0,3))
    elif config["Mining Direction"] == "Up" and await self.get_user_data("y")==63:
      await self.update_user_data("y", await self.get_user_data("y") + random.randrange(0,2))
    return True
  
    


    
