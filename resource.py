from asyncio.windows_events import NULL
from math import nan
import random
import user
import discord

def get_rarity_color(rarity):
  if rarity == "common":
    return 14671837
  elif rarity == "uncommon":
    return 7452273
  elif rarity == "rare":
    return 4092090
  elif rarity == "epic":
    return 13330369
  elif rarity == "legendary":
    return 16747803
  elif rarity == "mythic":
    return 16472355
  else:
    return None

class Item():
  pass

  

class Ore(Item):
  pass

class Pickaxe(Item):
  pass
  
class Wooden_Pickaxe(Pickaxe):
  emoji_id="<:Wooden_Pickaxe:954585728153698324>"
  catagory="Pickaxe"
  rarity="common"
  display_name="Wooden Pickaxe"
  def __init__(self):
    self.enchantments = {}
    self.durability = 59

class Stone_Pickaxe(Pickaxe):
  emoji_id="<:Stone_Pickaxe:954585728107544656>"
  catagory="Pickaxe"
  rarity="uncommon"
  display_name="Stone Pickaxe"
  def __init__(self):
    self.enchantments = {}
    self.durability = 131

class Iron_Pickaxe(Pickaxe):
  emoji_id="<:Iron_Pickaxe:954585728141111326>"
  catagory="Pickaxe"
  rarity="rare"
  display_name="Iron Pickaxe"
  def __init__(self):
    self.enchantments = {}
    self.durability = 250

class Golden_Pickaxe(Pickaxe):
  emoji_id="<:Golden_Pickaxe:954585728082378814>"
  catagory="Pickaxe"
  rarity="rare"
  display_name="Golden Pickaxe"
  def __init__(self):
    self.enchantments = {}
    self.durability = 32

class Diamond_Pickaxe(Pickaxe):
  emoji_id="<:Diamond_Pickaxe:954585728103362600>"
  catagory="Pickaxe"
  rarity="epic"
  display_name="Diamond Pickaxe"
  def __init__(self):
    self.enchantments = {}
    self.durability = 1561

class Netherite_Pickaxe(Pickaxe):
  emoji_id="<:Netherite_Pickaxe:954585728136925204>"
  catagory="Pickaxe"
  rarity="legendary"
  display_name="Netherite Pickaxe"
  def __init__(self):
    self.enchantments = {}
    self.durability = 2031


class Block(Item):
  pass
    
        


async def mine_loot(member):
  usr = user.User(member)
  y = await usr.get_user_data("y")
  choice = "".join(random.choices(list(event.keys()), get_dict_value(event)))
  if choice == "event":
    loot = ["event"]
  elif choice =="ore":
    if y <= 64 and y > 48:
      loot = random.choices(list(oreloot64.keys()), get_dict_value(oreloot64))
    elif y <= 48 and y > 32:
      loot = random.choices(list(oreloot48.keys()), get_dict_value(oreloot48)) 
    elif y <= 32 and y > 16:
      loot = random.choices(list(oreloot32.keys()), get_dict_value(oreloot32))  
    elif y <= 16 and y > 0:
      loot = random.choices(list(oreloot16.keys()), get_dict_value(oreloot16)) 
    elif y <= 0 and y > -16:
      loot = random.choices(list(oreloot0.keys()), get_dict_value(oreloot0))   
    elif y <= -16 and y > -32:
      loot = random.choices(list(oreloot_16.keys()), get_dict_value(oreloot_16))
    elif y <= -32 and y > -48:
      loot = random.choices(list(oreloot_32.keys()), get_dict_value(oreloot_32))  
    elif y <= -48 and y > -54:
      loot = random.choices(list(oreloot_48.keys()), get_dict_value(oreloot_48))     
    elif y <= -54 and y > -65:
      loot = random.choices(list(oreloot_54.keys()), get_dict_value(oreloot_54))      
    loot = "".join(loot)
  if loot == "event":
    embed = discord.Embed(title=f"{member.name}'s event", color=discord.Colour.gold())         
  else:
    multipler = await usr.get_multipler()
    await usr.change_y()
    name = items[loot]["name"]
    id = items[loot]["id"]
    rarity = items[loot]["rarity"]
    embed = discord.Embed(title=f"{member.name}'s booty", colour=get_rarity_color(rarity))
    embed.set_thumbnail(url="https://i.ibb.co/f8Lsxkb/Small-Mining-Sack.jpg")
    embed.add_field(value=f"You swung your pickaxe and got {multipler} {name} {id}", name='\u200b')
    y = await usr.get_user_data("y")
    embed.set_footer(text=f"new y-level ─ {y}")
      

    inventory = user.Inventory(member)
    await inventory.add_item(loot, multipler)
  return embed
    

items = {
  "Ore" : 
  {"Coal":{"emoji_id":"<:Coal:954584616734437486>", "rarity":"uncommon", "display_name":"Coal", "drop_multipler":1, "buy_price": int, "sell_price": int}, 
  "Copper_Ingot":{"emoji_id":"<:Copper_Ingot:954584616763789392>", "rarity":"uncommon","display_name":"Copper Ingot", "drop_multipler":random.randint(2,4), "buy_price": int, "sell_price" : int},
  "Iron_Ingot":{"emoji_id":"<:Iron_Ingot:954584616742846554>", "rarity":"uncommon", "display_name":"Iron Ingot"},  
  "Gold_Ingot":{"emoji_id":"<:Gold_Ingot:954584616738619462>", "rarity":"rare","display_name":"Gold Ingot"}, 
  "Lapis_Lazuli":{"emoji_id":"<:Lapis_Lazuli:954584616780570684>", "rarity":"epic","display_name":"Lapis"},
  "Redstone_Dust":{"emoji_id":"<:Redstone_Dust:954584616768004176>", "rarity":"rare","display_name":"Redstone"},
  "Diamond":{"emoji_id":"<:Diamond:954584616738635786>", "rarity":"legendary","display_name":"Diamond"}, 
  "Ruby":{"emoji_id":"<:Ruby:954584832866922526>", "rarity":"special","display_name":"Ruby"},
  "Emerald":{"emoji_id":"<:Emerald:954584616717660230>", "rarity":"epic","display_name":"Emerald"},
  "Gold_Nugget":{"emoji_id":"<:Gold_Nugget:954584616818335784>", "rarity":"uncommon","display_name":"Gold Nugget"},
  "Nether_Quartz":{"emoji_id":"<:Nether_Quartz:954584616730238986>", "rarity":"uncommon","display_name":"Quartz"},
  "Netherite_Ingot":{"emoji_id":"<:Netherite_Ingot:954584616835100762>", "rarity":"legendary","display_name":"Netherite Ingot"},
  },
  "Block":
  {
  "Cobblestone":{"emoji_id":"<:Cobblestone:955375789422047252>", "rarity":"common","display_name":"Cobblestone"},
  "Cobbled_Deepslate":{"emoji_id":"<:Cobbled_Deepslate:955375789484945408>", "rarity":"common","display_name":"Cobbled Deepslate"},
  "Netherrack":{"emoji_id":"<:Netherrack:954585851319431169>", "rarity":"common","display_name":"Netherrack"},
  "Blackstone":{"emoji_id":"<:Blackstone:954585850774163466>}", "rarity":"common","display_name":"Blackstone"},
  "Basalt":{"emoji_id":"<:Basalt:954585850782547979>", "rarity":"common","display_name":"Basalt"}
  }
}


loot_table = { 
"64_48" : {
"Cobblestone": 2014,
"Coal": 276, 
"Copper_Ingot": 216,
"Iron_Ingot": 30,  
"Lapis_Lazuli": 24,
"Emerald": 48
  }, 
"48_32" : {
"Cobblestone": 1936,
"Coal": 234, 
"Copper_Ingot": 294,
"Iron_Ingot": 84,  
"Lapis_Lazuli": 24,
"Emerald": 36
  }, 
"32_16" : {
"Cobblestone": 2092,
"Coal": 132, 
"Copper_Ingot": 216,
"Iron_Ingot": 114,  
"Lapis_Lazuli": 24,
"Emerald": 30
  }, 
"16_0" : {
"Cobblestone": 2014,
"Coal": 66, 
"Copper_Ingot": 174,
"Iron_Ingot": 264,  
"Gold_Ingot": 24,
"Lapis_Lazuli": 48,
"Emerald": 18
  }, 
"0_-16" : {
"Cobbled_Deepslate": 2170,
"Copper_Ingot": 72,
"Iron_Ingot": 162,  
"Gold_Ingot": 54,
"Lapis_Lazuli": 72,
"Redstone_Dust": 48,
"Diamond": 18, 
"Emerald": 12
  }, 
"-16_-32" : {
"Cobbled_Deepslate": 2304,
"Iron_Ingot": 84,  
"Gold_Ingot": 84,
"Lapis_Lazuli": 48,
"Redstone_Dust": 48,
"Diamond": 40
  },

"-32_-48" : {
"Cobbled_Deepslate": 2398,
"Iron_Ingot": 36,  
"Gold_Ingot": 54,
"Lapis_Lazuli": 24,
"Redstone_Dust": 48,
"Diamond": 48
  },

"-48_-54" : {
"Cobbled_Deepslate": 2316,
"Iron_Ingot": 30,  
"Gold_Ingot": 24,
"Lapis_Lazuli": 24,
"Redstone_Dust": 168,
"Diamond": 66, 
  },

"-54_-64" : {
"Cobbled_Deepslate": 2212,
"Iron_Ingot": 30,  
"Gold_Ingot": 48,
"Lapis_Lazuli": 24,
"Redstone_Dust": 216,
"Diamond": 78
  }
}

event = {"event": 6.284, "ore": 93.716}

def ore_drop_multipler(ore):
  pass




### NOT FINAL ONLY REFERENCE ###
#Redstone buy_price = 3, 
#Coal buy_price = 8
#Lapis buy_price = 5
#iron buy_price = 20 
#gold buy_price = 50 
#emerald buy_price = 100 
#diamond buy_price = 250 

"""Coal, diamond, emerald, their respective deepslate variants, and nether quartz ores drop 1 unit of their corresponding material.
Iron, gold, and their respective deepslate variants drop 1 unit of their raw form.
Copper and deepslate copper ores drop 2-5 raw copper.
Redstone and deepslate redstone ores drop 4–5 redstone dust.
Lapis lazuli and deepslate lapis lazuli ores drop 4–9 lapis lazuli.
Nether gold ore drops 2–6 gold nuggets.
Ancient debris is the exception; it drops itself when mined and must be smelted to obtain netherite scrap.

which means Fortune II gives 1.75x (13⁄4) drops on average, Fortune III gives 2.2x (21⁄5) drops on average, etc."""
