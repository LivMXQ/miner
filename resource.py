"This is OOP at its finest"
import random
import discord

class Event:
  pass

class MineOreEvent(Event):
  pass

class OtherEventLol(Event):
  pass
  
class Rarity:
  def get_color(self):
    return self.id
    
class Common(Rarity):
  id = 16777215

class Uncommon(Rarity):
  id = 5568851

class Rare(Rarity):
  id = 5592575

class Epic(Rarity):
  id = 11141801

class Legendary(Rarity):
  id = 16755200

class Mythic(Rarity):
  id = 16733694

class Special(Rarity):
  id = 14437965

class Item():
  def collection_embed(self):
    embed = discord.Embed(title="Yay")
    return embed

  def item_embed(self):
    embed = discord.Embed(title=self.__class__.display_name + " " + self.emoji_id, description=self.description)
    return embed

class Ore(Item):
  sellable = True

  def drop_multipler(self):
    return 1

class Coal(Ore):
  emoji_id = "<:Coal:954584616734437486>"
  rarity = Uncommon
  display_name = "Coal"
  buy_price = 120
  sell_price = 100
  description = None 

class Copper_Ingot(Ore):
  emoji_id = "<:Copper_Ingot:954584616763789392>"
  rarity = Uncommon
  display_name = "Copper"
  buy_price = 36
  sell_price = 30
  description = None
  
  def drop_multipler(self) -> int:
    return random.randint(2, 4) 
  
class Iron_Ingot(Ore):
  emoji_id = "<:Iron_Ingot:954584616742846554>"
  rarity = Uncommon
  display_name = "Iron"
  buy_price = 144 
  sell_price = 120
  description = None
  
class Gold_Ingot(Ore):
  emoji_id = "<:Gold_Ingot:954584616738619462>"
  rarity = Rare
  display_name = "Gold"
  buy_price = 318 
  sell_price = 289
  description = None
  
class Lapis_Lazuli(Ore):
  emoji_id = "<:Lapis_Lazuli:954584616780570684>"
  rarity = Rare
  display_name = "Lapis"
  buy_price = 53 
  sell_price = 44
  description = None
  
  def drop_multipler(self) -> int:
    return random.randint(4, 9) 
  
class Redstone_Dust(Ore):
  emoji_id = "<:Redstone_Dust:954584616768004176>"
  rarity = Rare
  display_name = "Redstone"
  buy_price = 46 
  sell_price = 38
  description = None
  
  def drop_multipler(self) -> int:
    return random.randint(4, 5) 
  
class Diamond(Ore):
  emoji_id = "<:Diamond:954584616738635786>"
  rarity = Epic
  display_name = "Diamond" 
  buy_price = 470 
  sell_price = 427
  description = None
  
class Ruby(Ore):
  sellable = False
  emoji_id = "<:Ruby:954584832866922526>"
  rarity = Special
  display_name = "Ruby"
  description = None
  
class Emerald(Ore):
  emoji_id = "<:Emerald:954584616717660230>"
  rarity = Rare
  display_name = "Emerald"
  buy_price = 530
  sell_price = 482
  description = None
  
class Gold_Nugget(Ore):
  sellable = False
  emoji_id = "<:Gold_Nugget:954584616818335784>"
  rarity = Uncommon
  display_name = "Gold Nugget"
  description = None
  
  def drop_multipler(self) -> int:
    return random.randint(2, 6) 
  
class Nether_Quartz(Ore):
  emoji_id = "<:Nether_Quartz:954584616730238986>"
  rarity = Uncommon
  display_name = "Quartz"
  buy_price = int 
  sell_price = int
  description = None
  
class Netherite_Ingot(Ore):
  emoji_id = "<:Netherite_Ingot:954584616835100762>"
  rarity = Legendary
  display_name = "Netherite"
  buy_price = int 
  sell_price = int
  description = None

class Pickaxe(Item):
  sellable = False
  def reduce_durability(self, number=1):
    self.durability -= number
  
  
class Wooden_Pickaxe(Pickaxe):
  emoji_id="<:Wooden_Pickaxe:954585728153698324>"
  catagory="Pickaxe"
  rarity=Common
  display_name="Wooden Pickaxe"
  description = None
  mining_speed = 2
  
  def __init__(self):
    self.enchantments = {}
    self.durability = 59

class Stone_Pickaxe(Pickaxe):
  emoji_id = "<:Stone_Pickaxe:954585728107544656>"
  catagory = "Pickaxe"
  rarity = Uncommon
  display_name  ="Stone Pickaxe"
  description = None
  mining_speed = 4
  
  def __init__(self):
    self.enchantments = {}
    self.durability = 131

class Iron_Pickaxe(Pickaxe):
  emoji_id = "<:Iron_Pickaxe:954585728141111326>"
  catagory = "Pickaxe"
  rarity = Rare
  display_name = "Iron Pickaxe"
  description = None
  mining_speed = 6
  
  def __init__(self):
    self.enchantments = {}
    self.durability = 250

class Golden_Pickaxe(Pickaxe):
  emoji_id = "<:Golden_Pickaxe:954585728082378814>"
  catagory = "Pickaxe"
  rarity = Rare
  display_name = "Golden Pickaxe"
  description = None
  mining_speed = 12
  
  def __init__(self):
    self.enchantments = {}
    self.durability = 32

class Diamond_Pickaxe(Pickaxe):
  emoji_id = "<:Diamond_Pickaxe:954585728103362600>"
  catagory = "Pickaxe"
  rarity = Epic
  display_name = "Diamond Pickaxe"
  description = None
  mining_speed = 8
  
  def __init__(self):
    self.enchantments = {}
    self.durability = 1561

class Netherite_Pickaxe(Pickaxe):
  emoji_id = "<:Netherite_Pickaxe:954585728136925204>"
  catagory = "Pickaxe"
  rarity = Legendary
  display_name = "Netherite Pickaxe"
  description = None
  mining_speed = 9
  
  def __init__(self):
    self.enchantments = {}
    self.durability = 2031


class Block(Item):
  sellable = True

  def drop_multipler(self) -> int:
    return 1

class Cobblestone(Block):
  emoji_id = "<:Cobblestone:955375789422047252>"
  rarity = Common
  display_name = "Cobblestone"
  buy_price = 12
  sell_price = 10
  description = None

class Cobbled_Deepslate(Block):
  emoji_id = "<:Cobbled_Deepslate:955375789484945408>"
  rarity = Common
  display_name = "Cobbled Deepslate"
  buy_price = 10
  sell_price = 8
  description = None

class Netherrack(Block):
  emoji_id = "<:Netherrack:954585851319431169>"
  rarity = Common
  display_name = "Netherrack"
  buy_price = int 
  sell_price = int
  description = None
  
class Blackstone(Block):
  emoji_id = "<:Blackstone:954585850774163466>"
  rarity = Common
  display_name = "Blackstone"
  buy_price = int 
  sell_price = int
  description = None
  
class Basalt(Block):
  emoji_id = "<:Basalt:954585850782547979>"
  rarity = Common
  display_name = "Basalt"
  buy_price = int 
  sell_price = int
  description = None
  
def get_y_section(y):
  if y <= 64 and y > 48:
    return "64_49"
  elif y <= 48 and y > 32:
    return "48_33"
  elif y <= 32 and y > 16:
    return "32_17"
  elif y <= 16 and y > 0:
    return "16_1"
  elif y <= 0 and y > -16:
    return "0_-15"
  elif y <= -16 and y > -32:
    return "-16_-31"
  elif y <= -32 and y > -48:
    return "-32_-47"
  elif y <= -48 and y > -54:
    return "-48_-53"
  elif y <= -54 and y > -65:
    return "-54_-64"

def get_dict_vlaues(dict):
  "return the keys and values in a dictionary as two lists"
  keys = []
  values = []
  for i in dict:
    keys.append(i)
    values.append(dict[i])
  return keys, values
    
loot_table = { 
"64_49" : {
Cobblestone: 2014,
Coal: 276, 
Copper_Ingot: 216,
Iron_Ingot: 30,  
Lapis_Lazuli: 24,
Emerald: 48
  }, 
"48_33" : {
Cobblestone: 1936,
Coal: 234, 
Copper_Ingot: 294,
Iron_Ingot: 84,  
Lapis_Lazuli: 24,
Emerald: 36
  }, 
"32_17" : {
Cobblestone: 2092,
Coal: 132, 
Copper_Ingot: 216,
Iron_Ingot: 114,  
Lapis_Lazuli: 24,
Emerald: 30
  }, 
"16_1" : {
Cobblestone: 2014,
Coal: 66, 
Copper_Ingot: 174,
Iron_Ingot: 264,  
Gold_Ingot: 24,
Lapis_Lazuli: 48,
Emerald: 18
  }, 
"0_-15" : {
Cobbled_Deepslate: 2170,
Copper_Ingot: 72,
Iron_Ingot: 162,  
Gold_Ingot: 54,
Lapis_Lazuli: 72,
Redstone_Dust: 48,
Diamond: 18, 
Emerald: 12
  }, 
"-16_-31" : {
Cobbled_Deepslate: 2304,
Iron_Ingot: 84,  
Gold_Ingot: 84,
Lapis_Lazuli: 48,
Redstone_Dust: 48,
Diamond: 40
  },

"-32_-47" : {
Cobbled_Deepslate: 2398,
Iron_Ingot: 36,  
Gold_Ingot: 54,
Lapis_Lazuli: 24,
Redstone_Dust: 48,
Diamond: 48
  },

"-48_-53" : {
Cobbled_Deepslate: 2316,
Iron_Ingot: 30,  
Gold_Ingot: 24,
Lapis_Lazuli: 24,
Redstone_Dust: 168,
Diamond: 66, 
  },

"-54_-64" : {
Cobbled_Deepslate: 2212,
Iron_Ingot: 30,  
Gold_Ingot: 48,
Lapis_Lazuli: 24,
Redstone_Dust: 216,
Diamond: 78
  }
}



"""
which means Fortune II gives 1.75x (13⁄4) drops on average, Fortune III gives 2.2x (21⁄5) drops on average, etc."""
