import discord
import random
import pickle
import resource as src
from replit import db


def get_all_users():
  return db["users"]

class Inventory:
  def __init__(self, user):
    self.user = user
    self.inv = db["users"][str(user.id)]["inventory"]

  def sort(self):
    self.inv.sort(lambda x:pickle.load(x).__class__.__name__)
    
  def add_item(self, item, amount):
    pickled = pickle.dumps(item, 0).decode()
    if pickled not in self.inv:
      self.inv[pickled] = amount
    else:     
      self.inv[pickled] += amount
    #for i in self.inv:
      #db["users"][str(self.user.id)]["inventory"][i] = self.inv[i]

  def remove_item(self, item, amount):
    if item not in self.inv:
      return False
    else:     
      self.inv[item] -= amount
    for i in self.inv:
      db["users"][str(self.user.id)]["inventory"][i] = self.inv[i]


class User: #all here
  def __init__(self, user):
    self.user = user

  
  def get_cooldown(self): #still working on this 
    return 17


  def get_multipler(self): #still working on this
    return 1

  def mine_(self):
    y = self.get_user_data("y")
    choice = random.choices([src.MineOreEvent, src.OtherEventLol], [93.716, 6.284])[0]
    if choice == src.MineOreEvent:
      ores, chances = src.get_dict_vlaues(src.loot_table[src.get_y_section(y)])
      loot = random.choices(ores, weights=chances)[0]
      multipler = self.get_multipler()
      change = self.change_y()
      embed = discord.Embed(title=f"{self.user.name}'s booty",description=f"You swung your pickaxe and got {multipler} {loot.display_name} {loot.emoji_id}", color=loot.rarity.id)
    
      new_y = y + change
      embed.set_footer(text=f"new y-level ─ {new_y}") 
      inventory = Inventory(self.user)
      inventory.add_item(loot, multipler)
    elif choice == src.OtherEventLol:
      embed = discord.Embed(title=f"{self.user.name}'s event", color=discord.Colour.gold())         
    return embed

  
  def return_to_base(self):
    if db["users"][str(self.user.id)]["y"] < 64:
      db["users"][str(self.user.id)]["y"] = 64
      return True
    else:
      return False
      
  async def create_account(self):
    pickaxe = src.Wooden_Pickaxe()
    db["users"][str(self.user.id)] = {'y': 64, 'inventory': {}, 'pickaxe': pickle.dumps(pickaxe, 0).decode(), 'configurations': {'Mining Direction': 'Down'}, "story":0}
    if isinstance(self.user, discord.Member):
      try:
        role = discord.utils.get(self.user.guild.roles, name="Minor ⛏️")
        await self.user.add_roles(role)
      except:
        print(f"WARN: Minor role not granted on account create")
    return True
    
  def update_user_data(self, type, *value):
    if self.check_if_in_db():
      if len(value) == 1:
        db["users"][str(self.user.id)][type] = value[0]
        return True
               
      elif len(value) == 2:
        db["users"][str(self.user.id)][type][value[0]] = value[1]
        return True
    else:
      return False
    
  def get_user_data(self, type):
    if self.check_if_in_db():
      value = db["users"][str(self.user.id)][type]
      return value
    else:
      return False

  def check_if_in_db(self):
    if str(self.user.id) in db["users"]:
      return True
    else:
      return False

  def delete_user(self):
    db["users"].pop(str(self.user.id))
    return True

  def change_y(self):
    config = self.get_user_data("configurations")
    y = self.get_user_data("y")
    if config["Mining Direction"] == "Down" and y >=-60:
      self.update_user_data("y", y - random.randrange(0,5))
    elif config["Mining Direction"] == "Down" and y==-61:
      self.update_user_data("y", y - random.randrange(0,4))
    elif config["Mining Direction"] == "Down" and y==-62:
      self.update_user_data("y", y - random.randrange(0,3))
    elif config["Mining Direction"] == "Down" and y==-63:
      self.update_user_data("y", y - random.randrange(0,2))
    elif config["Mining Direction"] == "Up" and y<=60:
      self.update_user_data("y", y + random.randrange(0,5))
    elif config["Mining Direction"] == "Up" and y==61:
      self.update_user_data("y", y + random.randrange(0,4))
    elif config["Mining Direction"] == "Up" and y==62:
      self.update_user_data("y", y + random.randrange(0,3))
    elif config["Mining Direction"] == "Up" and y==63:
      self.update_user_data("y", y + random.randrange(0,2))
    new_y = self.get_user_data("y")
    return new_y - y
  
    


    
