import random
"This is OOP at its finest"

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
  pass

class Ore(Item):
  pass

class Coal(Ore):
  emoji_id="<:Coal:954584616734437486>"
  rarity=Uncommon
  display_name="Coal"
  drop_multipler=1 
  buy_price=int
  sell_price=int 

class Copper_Ingot(Ore):
    emoji_id="<:Copper_Ingot:954584616763789392>"
    rarity=Uncommon
    display_name="Copper Ingot"
    drop_multipler=random.randint(2, 4) 
    buy_price=int 
    sell_price=int
  
class Iron_Ingot(Ore):
    emoji_id="<:Iron_Ingot:954584616742846554>"
    rarity=Uncommon
    display_name="Iron Ingot"
  
class Gold_Ingot(Ore):
    emoji_id="<:Gold_Ingot:954584616738619462>"
    rarity=Rare
    display_name="Gold Ingot"
  
class Lapis_Lazuli(Ore):
    emoji_id="<:Lapis_Lazuli:954584616780570684>"
    rarity=Rare
    display_name="Lapis"
  
class Redstone_Dust(Ore):
    emoji_id="<:Redstone_Dust:954584616768004176>"
    rarity=Rare
    display_name="Redstone"
  
class Diamond(Ore):
    emoji_id="<:Diamond:954584616738635786>"
    rarity=Epic
    display_name="Diamond" 
  
class Ruby(Ore):
    emoji_id="<:Ruby:954584832866922526>"
    rarity=Special
    display_name="Ruby"
  
class Emerald(Ore):
    emoji_id="<:Emerald:954584616717660230>"
    rarity=Rare
    display_name="Emerald"
  
class Gold_Nugget(Ore):
    emoji_id="<:Gold_Nugget:954584616818335784>"
    rarity=Uncommon
    display_name="Gold Nugget"
  
class Nether_Quartz(Ore):
    emoji_id="<:Nether_Quartz:954584616730238986>"
    rarity=Uncommon
    display_name="Quartz"
  
class Netherite_Ingot(Ore):
    emoji_id="<:Netherite_Ingot:954584616835100762>"
    rarity=Legendary
    display_name="Netherite Ingot"

class Pickaxe(Item):
  def reduce_durability(self, number=1):
    self.durability -= number
  
  
class Wooden_Pickaxe(Pickaxe):
  emoji_id="<:Wooden_Pickaxe:954585728153698324>"
  catagory="Pickaxe"
  rarity=Common
  display_name="Wooden Pickaxe"
  def __init__(self):
    self.enchantments = {}
    self.durability = 59

class Stone_Pickaxe(Pickaxe):
  emoji_id="<:Stone_Pickaxe:954585728107544656>"
  catagory="Pickaxe"
  rarity=Uncommon
  display_name="Stone Pickaxe"
  def __init__(self):
    self.enchantments = {}
    self.durability = 131

class Iron_Pickaxe(Pickaxe):
  emoji_id="<:Iron_Pickaxe:954585728141111326>"
  catagory="Pickaxe"
  rarity=Rare
  display_name="Iron Pickaxe"
  def __init__(self):
    self.enchantments = {}
    self.durability = 250

class Golden_Pickaxe(Pickaxe):
  emoji_id="<:Golden_Pickaxe:954585728082378814>"
  catagory="Pickaxe"
  rarity=Rare
  display_name="Golden Pickaxe"
  def __init__(self):
    self.enchantments = {}
    self.durability = 32

class Diamond_Pickaxe(Pickaxe):
  emoji_id="<:Diamond_Pickaxe:954585728103362600>"
  catagory="Pickaxe"
  rarity=Epic
  display_name="Diamond Pickaxe"
  def __init__(self):
    self.enchantments = {}
    self.durability = 1561

class Netherite_Pickaxe(Pickaxe):
  emoji_id="<:Netherite_Pickaxe:954585728136925204>"
  catagory="Pickaxe"
  rarity=Legendary
  display_name="Netherite Pickaxe"
  def __init__(self):
    self.enchantments = {}
    self.durability = 2031


class Block(Item):
  pass

class Cobblestone(Block):
  emoji_id="<:Cobblestone:955375789422047252>"
  rarity=Common
  display_name="Cobblestone"

class Cobbled_Deepslate(Block):
  emoji_id="<:Cobbled_Deepslate:955375789484945408>"
  rarity=Common
  display_name="Cobbled Deepslate"

class Netherrack(Block):
  emoji_id="<:Netherrack:954585851319431169>"
  rarity=Common
  display_name="Netherrack"
  
class Blackstone(Block):
  emoji_id="<:Blackstone:954585850774163466>"
  rarity=Common
  display_name="Blackstone"
  
class Basalt(Block):
  emoji_id="<:Basalt:954585850782547979>"
  rarity=Common
  display_name="Basalt"
  
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
