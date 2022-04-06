import random


def uncommon():
  return 7452273

def rare():
  return 4092090

def epic():
  return 13330369
  
def legendary():
  return 16747803

def mythic():
  return 16472355

class Item():
  def __init__(self, itemdict):
    self.id = itemdict["id"]
    self.rarity = itemdict["rarity"]
    self.catagory = itemdict["catagory"]
    self.allitems = allitems

  def getallitems(self):
    return self.allitems

  

class Ore(Item):
  def __init__(self):
    self.oredict = dict()
    for i in allitems:
      if allitems[i]["catagory"] == "ore":
        self.oredict[i] = allitems[i]

  def getores(self):
      return self.oredict

class Pickaxe(Item):
  def __init__(self):
    self.pickdict = {}
    for i in allitems:
      if allitems[i]["catagory"] == "pickaxe":
        self.pickdict[i] = allitems[i]

  def getpickaxes(self):
      return self.pickdict



class Block(Item):
  def __init__(self):
    self.blockdict = {}
    for i in allitems:
      if allitems[i]["catagory"] == "block":
        self.blockdict[i] = allitems[i]

  def getblocks(self):
      return self.blockdict
    
        



async def mine_loot(y):
  choice = "".join(random.choices(list(event.keys()), get_dict_value(event)))
  if choice == "event":
    return ["event"]
  elif choice =="ore":
    if y <= 64 and y > 48:
      loot = random.choices(list(oreloot64.keys()), get_dict_value(oreloot64))
      return loot
    elif y <= 48 and y > 32:
      loot = random.choices(list(oreloot48.keys()), get_dict_value(oreloot48))
      return loot
    elif y <= 32 and y > 16:
      loot = random.choices(list(oreloot32.keys()), get_dict_value(oreloot32))
      return loot
    elif y <= 16 and y > 0:
      loot = random.choices(list(oreloot16.keys()), get_dict_value(oreloot16))
      return loot
    elif y <= 0 and y > -16:
      loot = random.choices(list(oreloot0.keys()), get_dict_value(oreloot0))
      return loot
    elif y <= -16 and y > -32:
      loot = random.choices(list(oreloot_16.keys()), get_dict_value(oreloot_16))
      return loot
    elif y <= -32 and y > -48:
      loot = random.choices(list(oreloot_32.keys()), get_dict_value(oreloot_32))
      return loot
    elif y <= -48 and y > -54:
      loot = random.choices(list(oreloot_48.keys()), get_dict_value(oreloot_48))
      return loot
    elif y <= -54 and y > -65:
      loot = random.choices(list(oreloot_54.keys()), get_dict_value(oreloot_54))
      return loot
    

oreloot64 = {
"Cobblestone": 1476,
"Coal": 276, 
"Copper_Ingot": 216,
"Iron_Ingot": 30,  
"Lapis_Lazuli": 24,
"Emerald": 48
}

oreloot48 = {
"Cobblestone": 1398,
"Coal": 234, 
"Copper_Ingot": 294,
"Iron_Ingot": 84,  
"Lapis_Lazuli": 24,
"Emerald": 36
}

oreloot32 = {
"Cobblestone": 1398,
"Coal": 132, 
"Copper_Ingot": 216,
"Iron_Ingot": 114,  
"Lapis_Lazuli": 24,
"Emerald": 30
}

oreloot16 = {
"Cobblestone": 1476,
"Coal": 66, 
"Copper_Ingot": 174,
"Iron_Ingot": 264,  
"Gold_Ingot": 24,
"Lapis_Lazuli": 48,
"Emerald": 18
}

oreloot0 = {
"Cobbled_Deepslate": 1632,
"Copper_Ingot": 72,
"Iron_Ingot": 162,  
"Gold_Ingot": 54,
"Lapis_Lazuli": 72,
"Redstone_Dust": 48,
"Diamond": 18, 
"Emerald": 12
}

oreloot_16 = {
"Cobbled_Deepslate": 1766,
"Iron_Ingot": 84,  
"Gold_Ingot": 84,
"Lapis_Lazuli": 48,
"Redstone_Dust": 48,
"Diamond": 40
}

oreloot_32 = {
"Cobbled_Deepslate": 1860,
"Iron_Ingot": 36,  
"Gold_Ingot": 54,
"Lapis_Lazuli": 24,
"Redstone_Dust": 48,
"Diamond": 48
}

oreloot_48 = {
"Cobbled_Deepslate": 1758,
"Iron_Ingot": 30,  
"Gold_Ingot": 24,
"Lapis_Lazuli": 24,
"Redstone_Dust": 168,
"Diamond": 66, 
}

oreloot_54 = {
"Cobbled_Deepslate": 1674,
"Iron_Ingot": 30,  
"Gold_Ingot": 48,
"Lapis_Lazuli": 24,
"Redstone_Dust": 216,
"Diamond": 78
}


allitems = {"Coal":{"id":"<:Coal:954584616734437486>", "catagory":"Ore", "rarity":"uncommon", "name":"Coal"},
"Copper_Ingot":{"id":"<:Copper_Ingot:954584616763789392>", "catagory":"Ore", "rarity":"uncommon","name":"Copper Ingot"},
"Iron_Ingot":{"id":"<:Iron_Ingot:954584616742846554>", "catagory":"Ore", "rarity":"uncommon", "name":"Iron Ingot"},  
"Gold_Ingot":{"id":"<:Gold_Ingot:954584616738619462>", "catagory":"Ore", "rarity":"rare","name":"Gold Ingot"}, 
"Lapis_Lazuli":{"id":"<:Lapis_Lazuli:954584616780570684>", "catagory":"Ore", "rarity":"epic","name":"Lapis"},
"Redstone_Dust":{"id":"<:Redstone_Dust:954584616768004176>", "catagory":"Ore", "rarity":"rare","name":"Redstone"},
"Diamond":{"id":"<:Diamond:954584616738635786>",
"catagory":"Ore", "rarity":"legendary","name":"Diamond"}, 
"Ruby":{"id":"<:Ruby:954584832866922526>", 
"catagory":"Ore", "rarity":"special","name":"Ruby"},
"Emerald":{"id":"<:Emerald:954584616717660230>", "catagory":"Ore", "rarity":"epic","name":"Emerald"},
"Gold_Nugget":{"id":"<:Gold_Nugget:954584616818335784>", "catagory":"Ore", "rarity":"uncommon","name":"Gold Nugget"},
"Nether_Quartz":{"id":"<:Nether_Quartz:954584616730238986>", "catagory":"Ore", "rarity":"uncommon","name":"Quartz"},
"Netherite_Ingot":{"id":"<:Netherite_Ingot:954584616835100762>", "catagory":"Ore", "rarity":"legendary","name":"Netherite Ingot"},
"Wooden_Pickaxe":{"id":"<:Wooden_Pickaxe:954585728153698324>", "catagory":"Pickaxe", "rarity":"common","name":"Wooden Pickaxe"}, 
"Stone_Pickaxe":{"id":"<:Stone_Pickaxe:954585728107544656>", "catagory":"pickaxe", "rarity":"uncommon","name":"Stone Pickaxe"},
"Iron_Pickaxe":{"id":"<:Iron_Pickaxe:954585728141111326>", "catagory":"Pickaxe", "rarity":"rare","name":"Iron Pickaxe"},
"Golden_Pickaxe":{"id":"<:Golden_Pickaxe:954585728082378814>", 
"catagory":"Pickaxe", "rarity":"rare","name":"Golden Pickaxe"},
"Diamond_Pickaxe":{"id":"<:Diamond_Pickaxe:954585728103362600>", "catagory":"Pickaxe", "rarity":"epic","name":"Diamond Pickaxe"},
"Netherite_Pickaxe":{"id":"<:Netherite_Pickaxe:954585728136925204>", "catagory":"Pickaxe", "rarity":"legendary","name":"Netherite Pickaxe"},
"Cobblestone":{"id":"<:Cobblestone:955375789422047252>", "catagory":"Block", "rarity":"common","name":"Cobblestone"},
"Cobbled_Deepslate":{"id":"<:Cobbled_Deepslate:955375789484945408>", "catagory":"Block", "rarity":"common","name":"Cobbled Deepslate"},
"Netherrack":{"id":"<:Netherrack:954585851319431169>", "catagory":"Block", "rarity":"common","name":"Netherrack"},
"Blackstone":{"id":"<:Blackstone:954585850774163466>}", "catagory":"Block", "rarity":"common","name":"Blackstone"},
"Basalt":{"id":"<:Basalt:954585850782547979>", "catagory":"Block", "rarity":"common","name":"Basalt"}
}


event = {"event": 6.284, "ore": 93.716}


def get_dict_value(dict):
    list = []
    for key in dict:
        list.append(dict[key])
          
    return list
  
