import random

category = {
"ore" : {"Coal":"<:Coal:954584616734437486>", 
"Copper_Ingot":"<:Copper_Ingot:954584616763789392>",
"Iron_Ingot":"<:Iron_Ingot:954584616742846554>",  
"Gold_Ingot":"<:Gold_Ingot:954584616738619462>", "Lapis_Lazuli":"<:Lapis_Lazuli:954584616780570684>",
"Redstone_Dust":"<:Redstone_Dust:954584616768004176>",
"Diamond":"<:Diamond:954584616738635786>", 
"Ruby":"<:Ruby:954584832866922526>",
"Emerald":"<:Emerald:954584616717660230>",
"Gold_Nugget":"<:Gold_Nugget:954584616818335784>",
"Nether_Quartz":"<:Nether_Quartz:954584616730238986>",
"Netherite_Ingot":"<:Netherite_Ingot:954584616835100762>"
  },
             
"pickaxes" : {
"Wooden_Pickaxe":"<:Wooden_Pickaxe:954585728153698324>", 
"Stone_Pickaxe":"<:Stone_Pickaxe:954585728107544656> ",
"Iron_Pickaxe":"<:Iron_Pickaxe:954585728141111326>",
"Golden_Pickaxe":"<:Golden_Pickaxe:954585728082378814> ",
"Diamond_Pickaxe":"<:Diamond_Pickaxe:954585728103362600>",
"Netherite_Pickaxe":"<:Netherite_Pickaxe:954585728136925204>"
  },

"blocks" : {
"Cobblestone":"<:Cobblestone:955375789422047252>",
"Cobbled_Deepslate":"<:Cobbled_Deepslate:955375789484945408> ",
"Netherrack":"<:Netherrack:954585851319431169>",
"Blackstone":"<:Blackstone:954585850774163466>",
"Basalt":"<:Basalt:954585850782547979>"
  }
}

async def mine(y):
  choice = random.choices(list(event.keys()), get_dict_value(event))
  if choice == "event":
    return "event"
  else:
    if y <= 64 and y > 48:
      loot = random.choices(list(oreloot64.keys()), get_dict_value(oreloot64))
      return loot
    elif y <= 48 and y > 32:
      loot = random.choices(list(oreloot48.keys()), get_dict_value(oreloot64))
      return loot
    elif y <= 32 and y > 16:
      loot = random.choices(list(oreloot32.keys()), get_dict_value(oreloot64))
      return loot
    elif y <= 16 and y > 0:
      loot = random.choices(list(oreloot16.keys()), get_dict_value(oreloot64))
      return loot
    elif y <= 0 and y > -16:
      loot = random.choices(list(oreloot0.keys()), get_dict_value(oreloot64))
      return loot
    elif y <= -16 and y > -32:
      loot = random.choices(list(oreloot_16.keys()), get_dict_value(oreloot64))
      return loot
    elif y <= -32 and y > -48:
      loot = random.choices(list(oreloot_32.keys()), get_dict_value(oreloot64))
      return loot
    elif y <= -48 and y > -54:
      loot = random.choices(list(oreloot_48.keys()), get_dict_value(oreloot64))
      return loot
    elif y <= -54 and y > -65:
      loot = random.choices(list(oreloot_54.keys()), get_dict_value(oreloot64))
      return loot
    else:
      return "Heh what happened to ur y level"
    

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


event = {"event": 3.142, "ore": 96.858}

def get_all_items():
  allitemdict = {}
  for key in category:
        categorydict = category[key]
        for cey in categorydict:
          allitemdict[cey] = categorydict[cey]
  return allitemdict

def get_dict_value(dict):
    list = []
    for key in dict:
        list.append(dict[key])
          
    return list
  
def random_color():
  hexadecimal = int("0x"+"".join([random.choice('ABCDEF0123456789') for i in range(6)]), 16)
  return hexadecimal

allitemdict = get_all_items()