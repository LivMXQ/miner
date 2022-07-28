"sdk"
import discord
import os
import random
import pickle
import resource as src
from replit import Database

bot_colour = int(os.getenv("COLOUR"))

db = Database(os.getenv("REPLIT_DB_URL"))
if "users" not in db.keys():
  db["users"] = dict()
  
registeredviews = list()
currentview = None
pickaxe = src.Wooden_Pickaxe()
default_dictionary = {
  'y': 64, 
  'inventory': {}, 
  "collection": {}, 
  'pickaxe': pickle.dumps(pickaxe, 0).decode(), 
  "experience": 0, 
  'configurations': {'mining_direction': 'down', "inventory_key":"by_name"}, 
  "story":0,
  "streak":0
  }

class User: 
  def __init__(self, user=None, ctx=None):
    self.ctx = ctx
    if user:
      self.user = user
    elif ctx:
      self.user = ctx.author
    else:
      self.user = None
    self.data = self.get_user_data() #ONYL USE THIS TO READ DATA

  def get_cooldown(self):
    return 17


  def get_multipler(self): 
    return 1

  async def create_account(self):
    db["users"][str(self.user.id)] = default_dictionary
    return True

  async def send_collection_message(self):
    default = "Block"
    catagory = get_class(default, src.Item.__subclasses__())
    shop_view = ViewTimeout(ctx=self.ctx, timeout=20)

    def collection_embed(catagory):
      desc = []
      for i in catagory.__subclasses__(): 
        amount = 0
        if i.__name__ in self.data["collection"]:
          amount = self.data["collection"][i.__name__]
        level = calculate_level(amount)
        desc.append(f"{i.emoji_id} `{amount}/{src.collection_levels[level]}` **{i.display_name} {roman(level)}**")
      embed = discord.Embed(title=catagory.__name__+" Collections", description="\n".join(desc), colour=bot_colour)
      return embed
    
    class ShopSelect(discord.ui.Select):
      def __init__(self): 
        super().__init__(options=[discord.SelectOption(label=i.__name__) for i in src.Item.__subclasses__() if i.__name__ != "Pickaxe"])

      async def callback(self, interaction):
        catagory = get_class(self.values[0], src.Item.__subclasses__())
        await interaction.response.edit_message(embed=collection_embed(catagory))   
    shop_select = ShopSelect()
    shop_view.add_item(shop_select)
    shop_view.message = await self.ctx.send(embed=collection_embed(catagory), view=shop_view)

  async def mine_(self):
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
      await self.ctx.send(embed=embed)
      self.inventory_add(loot, multipler)
      await self.collection_add(loot, multipler, self.ctx)
    elif choice == src.OtherEventLol:
      embed = discord.Embed(title=f"{self.user.name}'s event", color=discord.Colour.gold())
      await self.ctx.send(embed=embed)

  async def send_inventory_message(self):
    self.sort_inventory(self.data["configurations"]["inventory_key"])
    value = []
    for i in self.data["inventory"]:
      if self.data["inventory"] != 0:
        item = get_class(i, get_all_items(), key="name")
        value.append(f'{item.emoji_id} **{item.display_name}** × {self.data["inventory"][i]}')
    embed = discord.Embed(title=f"{self.user.name}'s Inventory", description="\n".join(value), colour=bot_colour)
    embed.set_footer(text="You can't use 'pls use [item]' to use an item lol")
    await self.ctx.send(embed=embed)

  def return_to_base(self):
    if self.data["y"] < 64:
      db["users"][str(self.user.id)]["y"] = 64
      return True
    else:
      return False
    
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

  def change_y(self) -> int:
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
      keys.sort(key=lambda x: x)    
      db["users"][str(self.user.id)]["inventory"] = dict(zip(keys,[self.data["inventory"][i] for i in keys]))

  def inventory_add(self, item, amount):
    _item = item.__name__
    if _item not in self.data["inventory"]:
      db["users"][str(self.user.id)]["inventory"][_item] = amount
    else:     
      db["users"][str(self.user.id)]["inventory"][_item] += amount

  async def collection_add(self, item, amount, ctx):
    _item = item.__name__
    if _item not in self.data["collection"]:
      db["users"][str(self.user.id)]["collection"][_item] = amount
      unlock_embed = discord.Embed(title="✨ NEW COLLECTION UNLOCKED ✨", description=item.emoji_id + item.display_name, colour=item.rarity.id)
      await self.ctx.send(embed=unlock_embed)
      return 1   
    else:     
      oamount = self.data["collection"][_item]
      olevel = calculate_level(oamount)
      newlevel = calculate_level(oamount+amount)
      db["users"][str(self.user.id)]["collection"][_item] += amount
      if newlevel != olevel:
        levelup_embed = discord.Embed(title="✨ COLLECTION LEVEL UP ✨", description=item.emoji_id+item.display_name+" "+roman(newlevel), colour=item.rarity.id)
        await self.ctx.send(embed=levelup_embed)
        return 2
      return 0
  
  def inventory_remove(self, item, amount):
    if item not in self.data["inventory"]:
      return False
    else:     
      db["users"][str(self.user.id)]["inventory"][item] -= amount

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
    
class endinteractionbtn(discord.ui.Button):
    def __init__(self, row=1):
      super().__init__(label="End Interaction")

    async def callback(self, interaction):
      await currentview.disable_all()
      await interaction.response.edit_message(view=currentview)


class ViewTimeout(discord.ui.View):
  def __init__(self, ctx, timeout=10):
    super().__init__(timeout=timeout)
    self.inactive = False
    self.ctx = ctx

  async def on_timeout(self):
    if self.inactive == False:
      self.disable_all_items()
      await self.message.edit(view=self)

  async def interaction_check(self, interaction: discord.Interaction):
    if interaction.user != self.ctx.author:
      await interaction.response.send_message("That's not your miner bro", ephemeral=True)
      return False
    else:
      return True

def roman(number):
  num = [1, 4, 5, 9, 10, 40, 50, 90,
        100, 400, 500, 900, 1000]
  sym = ["I", "IV", "V", "IX", "X", "XL",
        "L", "XC", "C", "CD", "D", "CM", "M"]
  i = 12
  value = []
  if number == 0:
    return "0"  
  while number:
    div = number // num[i]
    number %= num[i]
  
    while div:
      value.append(sym[i])
      div -= 1
    i -= 1
  return "".join(value)

def calculate_level(number, num=src.collection_levels) -> int:
  "return a level based on the total amount and the intervals"
  level = 0

  for i in num:
    if number >= i:
      level += 1
    
  return level

def get_class(name, list, key="name"):
  "returns the class with the name given within a list of classes"
  if key == "name":
    for i in list:
      if i.__name__ == name:
        return i
    return
  elif key == "display_name":
    for i in list:
      if i.display_name == name:
        return i
    return

def get_all_users():
  return db["users"]

def get_all_items() -> list:
  "returns a list of all the items"
  item_list = []
  for i in src.Item.__subclasses__():
    for j in i.__subclasses__():
      item_list.append(j)
  return item_list

def initialize_cooldowns(cooldowns_):
  if db["users"]:
    for i in db["users"]:
      user_id = i
      duration = 17.5
      cooldowns_[user_id] = discord.ext.commands.CooldownMapping.from_cooldown(1, duration, discord.ext.commands.BucketType.user)  