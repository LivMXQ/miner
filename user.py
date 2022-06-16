import discord
import random
import pickle
import resource as src
from replit import db

pickaxe = src.Wooden_Pickaxe()
default_dictionary = {'y': 64, 'inventory': {}, 'pickaxe': pickle.dumps(pickaxe, 0).decode(), 'configurations': {'mining_direction': 'Down', "inventory_key":"by_name"}, "story":0}

def get_all_users():
  return db["users"]


class User: #all here
  def __init__(self, user):
    self.user = user
    self.data = db["users"][str(user.id)]
    self.inv = db["users"][str(user.id)]["inventory"]

  
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
      self.add_item_to_inventory(loot, multipler)
    elif choice == src.OtherEventLol:
      embed = discord.Embed(title=f"{self.user.name}'s event", color=discord.Colour.gold())
    return embed

  
  def return_to_base(self):
    if self.data["y"] < 64:
      self.data["y"] = 64
      return True
    else:
      return False
      
  async def create_account(self):
    self.data = default_dictionary
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
        self.data[type] = value[0]
        return True
               
      elif len(value) == 2:
        self.data[type][value[0]] = value[1]
        return True
    else:
      return False
    
  def get_user_data(self, type):
    if self.check_if_in_db():
      value = self.data[type]
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
    if config["mining_direction"] == "Down" and y >=-60:
      self.update_user_data("y", y - random.randrange(0,5))
    elif config["mining_direction"] == "Down" and y==-61:
      self.update_user_data("y", y - random.randrange(0,4))
    elif config["mining_direction"] == "Down" and y==-62:
      self.update_user_data("y", y - random.randrange(0,3))
    elif config["mining_direction"] == "Down" and y==-63:
      self.update_user_data("y", y - random.randrange(0,2))
    elif config["mining_direction"] == "Up" and y<=60:
      self.update_user_data("y", y + random.randrange(0,5))
    elif config["mining_direction"] == "Up" and y==61:
      self.update_user_data("y", y + random.randrange(0,4))
    elif config["mining_direction"] == "Up" and y==62:
      self.update_user_data("y", y + random.randrange(0,3))
    elif config["mining_direction"] == "Up" and y==63:
      self.update_user_data("y", y + random.randrange(0,2))
    new_y = self.get_user_data("y")
    return new_y - y
  
  def sort_inventory(self, key="by_name"):
    if key=="by_name":
      keys = [i for i in self.inv.keys()]
      keys.sort(key=lambda x: pickle.loads(x.encode()).__name__)    
      self.inv = dict(zip(keys,[self.inv[i] for i in keys]))

    
  def add_item_to_inventory(self, item, amount):
    pickled = pickle.dumps(item, 0).decode()
    if pickled not in self.inv:
      self.inv[pickled] = amount
    else:     
      self.inv[pickled] += amount
  
  def remove_item_from_inventory(self, item, amount):
    if item not in self.inv:
      return False
    else:     
      self.inv[item] -= amount

  def update_default_dict(self):
    counter = 0
    for a in default_dictionary:
      if a not in self.data.keys():
        self.data[a] = default_dictionary[a]
        counter +=1
    for b in default_dictionary["configurations"]:
      if b not in self.data["configurations"]:
        self.data["configurations"][b] = default_dictionary["configurations"][b]
        counter +=1
    return counter
    
