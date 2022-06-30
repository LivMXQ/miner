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
    self.data = self.get_user_data() #ONYL USE THIS TO READ DATA

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
      multipler = self.get_multipler() * loot().drop_multipler()
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
      db["users"][str(self.user.id)]["y"] = 64
      return True
    else:
      return False
      
  async def create_account(self):
    db["users"][str(self.user.id)] = default_dictionary
    if isinstance(self.user, discord.Member):
      try:
        role = discord.utils.get(self.user.guild.roles, name="Minor ⛏️")
        await self.user.add_roles(role)
      except:
        print(f"WARN: Minor role not granted on account create")
    return True
    
  def update_user_data(self, value, *type):
    if self.check_if_in_db():
      if len(type) == 0:
        db["users"][str(self.user.id)] = value
        return True
      elif len(type) == 1:
        db["users"][str(self.user.id)][type[0]] = value
        return True        
      elif len(type) == 2:
        db["users"][str(self.user.id)][type[0]][type[1]] = value
        return True
    else:
      return False
    
  def get_user_data(self, *type):
    if self.check_if_in_db():
      if len(type) == 0:
        value = db["users"][str(self.user.id)] 
        return value
      elif len(type) == 1:
        value = db["users"][str(self.user.id)][type[0]] 
        return value        
      elif len(type) == 2:
        value = db["users"][str(self.user.id)][type[0]][type[1]] 
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
    config = self.data["configurations"]
    y = self.data["y"]
    if config["mining_direction"] == "down":
      db["users"][str(self.user.id)]["y"] = y - random.randint(0,4)
    elif config["mining_direction"] == "up":
      db["users"][str(self.user.id)]["y"] = y + random.randint(0,4)
    new_y = self.data["y"]
    if new_y > 64:
      db["users"][str(self.user.id)]["y"] = 64
    if new_y < -64:
      db["users"][str(self.user.id)]["y"] = -64
    return new_y - y
  
  def sort_inventory(self, key="by_name"):
    if key=="by_name":
      keys = [i for i in self.data["inventory"].keys()]
      keys.sort(key=lambda x: pickle.loads(x.encode()).__name__)    
      db["users"][str(self.user.id)]["inventory"] = dict(zip(keys,[self.data["inventory"][i] for i in keys]))

    
  def add_item_to_inventory(self, item, amount):
    pickled = pickle.dumps(item, 0).decode()
    if pickled not in self.data["inventory"]:
      db["users"][str(self.user.id)]["inventory"][pickled] = amount
    else:     
      db["users"][str(self.user.id)]["inventory"][pickled] += amount
  
  def remove_item_from_inventory(self, item, amount):
    if item not in self.data["inventory"]:
      return False
    else:     
      db["users"][str(self.user.id)]["inventory"][item] -= amount

  def get_inventory_embed(self):
    self.sort_inventory(self.get_user_data("configurations", "inventory_key"))
    value = []
    for i in self.data["inventory"]:
      if self.data["inventory"] != 0:
        item = pickle.loads(i.encode())
        value.append(f"""{item.emoji_id} **{item.display_name}** × {self.data["inventory"][i]}""")
    embed = discord.Embed(title=f"{self.user.name}'s Inventory", description="\n".join(value), colour=6671615)
    embed.set_footer(text="You can't use 'pls use [item]' to use an item lol")
    return embed

  def update_default_dict(self):
    counter = 0
    for a in default_dictionary:
      if a not in self.data.keys():
        db["users"][str(self.user.id)][a] = default_dictionary[a]
        counter +=1
    for b in default_dictionary["configurations"]:
      if b not in self.data["configurations"]:
        db["users"][str(self.user.id)]["configurations"][b] = default_dictionary["configurations"][b]
        counter +=1
    return counter
    
