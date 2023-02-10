from dataclasses import dataclass
from collections import namedtuple
from json import load as jload
from json import JSONDecodeError
from pathlib import Path
from typing import NewType, Dict, List
from itertools import islice
from itertools import product as it_product
from time import perf_counter
import numpy as np
import json


@dataclass
class Cooker:
    oven: int = 178
    forge: int = 180
    campfire: int = 37

    @staticmethod
    def get_cookers(cookers:List[str])->List[tuple[str, int]]:
        # {"cooker": ["oven","rare oven"]},
        a = []
        for v in cookers:
            cooker = ""
            rarity = 0
            if "rare" in v:
                cooker = v[5:]
                rarity = 1
            elif "supreme" in v:
                cooker = v[8:]
                rarity = 2
            elif "fantastic" in v:
                cooker = v[10:]
                rarity = 3
            else:
                cooker = v
            b = eval("Cooker."+cooker)
            a.append([v, (b + rarity) % 138])
        return a

@dataclass
class Rarity:
    rare: int = 1
    supreme: int = 2
    fantastic: int = 3

@dataclass
class Container:
    pottery_bowl: int = 77
    frying_pan: int = 75
    cauldron: int = 351
    plate: int = 1173
    roasting_dish: int = 1169
    baking_stone: int = 1167

    @staticmethod
    def get_container(containers:List[str])->List[tuple[str, int]]:
        # {"container": ["cauldron"]},
        a = []
        for v in containers:
            b = eval("Container."+v)
            a.append([v, b % 138])
        return a

@dataclass
class Material:
    UNDEFINED: int = 0
    flesh: int = 1
    meat: int = 2
    rye: int = 3
    oat: int = 4
    barley: int = 5
    wheat: int = 6
    gold: int = 7
    silver: int = 8
    steel: int = 9
    copper: int = 10
    iron: int = 11
    lead: int = 12
    zinc: int = 13
    birchwood: int = 14
    stone: int = 15
    leather: int = 16
    cotton: int = 17
    clay: int = 18
    pottery: int = 19
    glass: int = 20
    magic: int = 21
    vegetarian: int = 22
    fire: int = 23
    oil: int = 25
    water: int = 26
    charcoal: int = 27
    dairy: int = 28
    honey: int = 29
    brass: int = 30
    bronze: int = 31
    fat: int = 32
    paper: int = 33
    tin: int = 34
    bone: int = 35
    salt: int = 36
    pinewood: int = 37
    oakenwood: int = 38
    cedarwood: int = 39
    willow: int = 40
    maplewood: int = 41
    applewood: int = 42
    lemonwood: int = 43
    olivewood: int = 44
    cherrywood: int = 45
    lavenderwood: int = 46
    rosewood: int = 47
    thorn: int = 48
    grapewood: int = 49
    camelliawood: int = 50
    oleanderwood: int = 51
    crystal: int = 52
    wemp: int = 53
    diamond: int =54 
    animal: int = 55
    adamantine: int = 56
    glimmersteel: int = 57
    tar: int = 58
    peat: int = 59
    reed: int = 60
    slate: int = 61
    marble: int = 62
    chestnut: int = 63
    walnut: int = 64
    firwood: int = 65
    lindenwood: int = 66 
    seryll: int = 67
    ivy: int = 68
    wool: int = 69
    straw: int = 70
    hazelnutwood: int = 71
    bear: int = 72
    beef: int = 73
    canine: int = 74
    feline: int = 75
    dragon: int = 76
    fowl: int = 77
    game: int = 78
    horse: int = 79
    human: int = 80
    humanoid: int = 81 
    insect: int = 82
    lamb: int = 83
    pork: int = 84
    seafood: int = 85 
    snake: int = 86
    tough: int = 87
    orangewood: int = 88
    sandstone: int = 89
    raspberrywood: int = 90
    blueberrywood: int = 91
    lingonberrywood: int = 92
    metal: int = 93 # MATERIAL_METALFRAG_BASE
    alloy: int = 94 # MATERIAL_METALFRAG_ALLOY
    moonmetal: int = 95 # MATERIAL_METALFRAG_MOON 
    electrum: int = 96

@dataclass
class State:
    raw: int = 0
    fried: int = 1
    grilled: int = 2
    boiled: int = 3
    roasted: int = 4
    steamed: int = 5
    baked: int = 6
    cooked: int = 7
    candied: int = 8
    chocolate_coated: int = 9
    chopped: int = 16
    diced: int = 16
    ground: int = 16
    unfermented: int = 16
    zombiefied: int = 16
    whipped: int = 16
    mashed: int = 32
    minced: int = 32
    fermenting: int = 32
    clotted: int = 32
    wrapped: int = 64
    undistilled: int = 64
    salted: int = -128
    salty: int =-128
    fresh: int = -128
    live: int = -128
    
    @staticmethod
    def get_names()-> tuple[str]:
        a = ('raw', 'fried', 'grilled', 'boiled', 'roasted', 'steamed', 'baked', 'cooked', 'candied', 'chocolate coated', 'chopped', 'diced', 'ground', \
            'unfermented', 'zombiefied', 'whipped', 'mashed', 'minced', 'fermenting', 'clotted', 'wrapped', 'undistilled', 'salted', 'salty', 'fresh', 'live')
        return a
    
  
    @staticmethod
    def get_state(s:list[str])-> tuple[str, int]:
        ing = ""
        if s[0] == "chocolate" and s[1] == "coated":
            ing = " ".join([v for v in islice(s,2, len(s))])
            off = State.chocolate_coated
            return ing, off
        n = State.get_names()
        if s[0] in n:
            off = eval("State."+s[0]) 
            ing = " ".join([v for v in islice(s,1, len(s))])
            return ing, off
        else:
            ing = " ".join(s)
            return ing, 0

Ingredient = namedtuple('Ingredient', ['template', 'material', 'real', 'state'], defaults=[0,0,0,0])

@dataclass
class Ingredients:
    """
    # modulo'd all summed values(template ID + template material ID + real template ID + state) by 138.
    """
    # veggie
    pea: Ingredient = Ingredient(template=1150, material=Material.vegetarian, real=-10)
    corn: Ingredient = Ingredient(template=32, material=Material.vegetarian, real=-10)
    garlic: Ingredient = Ingredient(template=356, material=Material.vegetarian, real=-10)
    tomato: Ingredient = Ingredient(template=1135, material=Material.vegetarian, real=-10)
    pea_pods: Ingredient = Ingredient(template=1138, material=Material.vegetarian, real=-10)
    carrot: Ingredient = Ingredient(template=1133, material=Material.vegetarian, real=-10)
    cucumber: Ingredient = Ingredient(template=1247, material=Material.vegetarian, real=-10)
    onion: Ingredient = Ingredient(template=355, material=Material.vegetarian, real=-10)
    potato: Ingredient = Ingredient(template=35, material=Material.vegetarian, real=-10)
    lettuce: Ingredient = Ingredient(template=1137, material=Material.vegetarian, real=-10)
    pumpkin: Ingredient = Ingredient(template=33, material=Material.vegetarian, real=-10)
    cabbage: Ingredient = Ingredient(template=1134, material=Material.vegetarian, real=-10)

    # meat
    meat_bear: Ingredient =  Ingredient(template=92, material=Material.bear, real=-10)
    meat_beef: Ingredient = Ingredient(template=92, real=-10, material=Material.beef) 
    meat_canine: Ingredient = Ingredient(template=92, real=-10, material=Material.canine) 
    meat_feline: Ingredient = Ingredient(template=92, real=-10, material=Material.feline) 
    meat_dragon: Ingredient = Ingredient(template=92, real=-10, material=Material.dragon) 
    meat_fowl: Ingredient = Ingredient(template=92, real=-10, material=Material.fowl) 
    meat_game: Ingredient = Ingredient(template=92, real=-10, material=Material.game) 
    meat_horse: Ingredient = Ingredient(template=92, real=-10, material=Material.horse) 
    meat_human: Ingredient = Ingredient(template=92, real=-10, material=Material.human) 
    meat_humanoid: Ingredient = Ingredient(template=92, real=-10, material=Material.humanoid) 
    meat_insect: Ingredient = Ingredient(template=92, real=-10, material=Material.insect) 
    meat_lamb: Ingredient = Ingredient(template=92, real=-10, material=Material.lamb) 
    meat_pork: Ingredient = Ingredient(template=92, real=-10, material=Material.pork) 
    meat_seafood: Ingredient = Ingredient(template=92, real=-10, material=Material.seafood) 
    meat_snake: Ingredient = Ingredient(template=92, real=-10, material=Material.snake) 
    meat_tough: Ingredient = Ingredient(template=92, real=-10, material=Material.tough)

    # herbs
    lovage: Ingredient = Ingredient(real=-10, material=Material.vegetarian, template=353) 
    rosemary: Ingredient = Ingredient(real=-10, material=Material.vegetarian, template=363)
    basil: Ingredient = Ingredient(real=-10, material=Material.vegetarian, template=359)
    belladonna: Ingredient = Ingredient(real=-10, material=Material.vegetarian, template=361)
    mint: Ingredient = Ingredient(real=-10, material=Material.vegetarian, template=1130)
    oregano: Ingredient = Ingredient(real=-10, material=Material.vegetarian, template=357)
    parsley: Ingredient = Ingredient(real=-10, material=Material.vegetarian, template=358)
    sage: Ingredient = Ingredient(real=-10, material=Material.vegetarian, template=354)
    thyme: Ingredient = Ingredient(real=-10, material=Material.vegetarian, template=360)
    fennelPlant: Ingredient = Ingredient(real=-10, material=Material.vegetarian, template=1132)
    # harder to get herbs
    sassafras: Ingredient = Ingredient(real=-10, material=Material.vegetarian, template=366)
    nettles: Ingredient = Ingredient(real=-10, material=Material.vegetarian, template=365)
    # forestry item
    camellia: Ingredient = Ingredient(real=-10, material=Material.vegetarian, template=422)
    # spice
    fennelSeed: Ingredient = Ingredient(real=-10, material=Material.vegetarian, template=1151)
    cumin: Ingredient = Ingredient(real=-10, material=Material.vegetarian, template=1140)
    paprika: Ingredient = Ingredient(real=-10, material=Material.vegetarian, template=1143)
    turmeric: Ingredient = Ingredient(real=-10, material=Material.vegetarian, template=1144)
    ginger: Ingredient = Ingredient(real=-10, material=Material.vegetarian, template=1141)
    # cheeses
    cheese: Ingredient = Ingredient(real=-10, material=Material.dairy, template=66) 
    buffalo_cheese: Ingredient = Ingredient(real=-10, material=Material.dairy, template=69) 
    feta_cheese: Ingredient = Ingredient(real=-10, material=Material.dairy, template=68)
    #water
    water: Ingredient = Ingredient(real=-10, material=Material.water, template=128) 
    #salty_water: Ingredient = Ingredient(real=-10, material=Material.water, template=128, state=State.salted)
    
    sugar: Ingredient = Ingredient(real=-10, material=Material.vegetarian, template=1139)
    maple_syrup: Ingredient = Ingredient(real=-10, material=Material.water, template=415)
    honey: Ingredient = Ingredient(real=-10, material=Material.honey, template=70)
    #grains
    wheat: Ingredient = Ingredient(real=-10, material=Material.wheat, template=29)
    barley: Ingredient = Ingredient(real=-10, material=Material.barley, template=28)
    oat: Ingredient = Ingredient(real=-10, material=Material.oat, template=31)
    rye: Ingredient = Ingredient(real=-10, material=Material.rye, template=30)
    #breads
    waybread_wheat: Ingredient = Ingredient(real=70, material=Material.wheat, template=203, state=State.salted)
    waybread_barley: Ingredient = Ingredient(real=70, material=Material.barley, template=203, state=State.salted)
    waybread_oat: Ingredient = Ingredient(real=70, material=Material.oat, template=203, state=State.salted)
    waybread_rye: Ingredient = Ingredient(real=70, material=Material.rye, template=203, state=State.salted)


    @staticmethod
    def get_ingredient(ingredients:List[str])->List[tuple[str, int]]:
        #{"ingredients": ["roasted pea", "fried pea"]},
        a = []
        for v in ingredients:
            w = v.split(" ")
            if len(w) > 1:
                nam, off = State.get_state(w)
                nam = nam.replace(" ", "_")
            else:
                nam = v
                off = 0
            ing_type = NewType("ing_type", Ingredient)
            ing = ing_type(eval("Ingredients." + nam))
            a.append([v, (ing.template + ing.real + ing.material + off) % 138])
        return a

def get_skill_name(i: int):
    if i == 1:
        return 'Mind'
    elif i == 2:
        return 'Body'
    elif i == 3:
        return 'Soul'
    elif i == 4:
        return 'Body control'
    elif i == 5:
        return 'Body stamina'
    elif i == 6:
        return 'Body strength'
    elif i == 7:
        return 'Mind logic'
    elif i == 8:
        return 'Mind speed'
    elif i == 9:
        return 'Soul depth'
    elif i == 10:
        return 'Soul strength'
    elif i == 11:
        return 'Swords'
    elif i == 12:
        return 'Axes'
    elif i == 13:
        return 'Knives'
    elif i == 14:
        return 'Mauls'
    elif i == 15:
        return 'Clubs'
    elif i == 16:
        return 'Hammers'
    elif i == 17:
        return 'Archery'
    elif i == 18:
        return 'Polearms'
    elif i == 19:
        return 'Tailoring'
    elif i == 20:
        return 'Cooking'
    elif i == 21:
        return 'Smithing'
    elif i == 22:
        return 'Weapon smithing'
    elif i == 23:
        return 'Armour smithing'
    elif i == 24:
        return 'Miscellaneous items'
    elif i == 25:
        return 'Shields'
    elif i == 26:
        return 'Alchemy'
    elif i == 27:
        return 'Nature'
    elif i == 28:
        return 'Toys'
    elif i == 29:
        return 'Fighting'
    elif i == 30:
        return 'Healing'
    elif i == 31:
        return 'Religion'
    elif i == 32:
        return 'Thievery'
    elif i == 33:
        return 'War machines'
    elif i == 34:
        return 'Farming'
    elif i == 35:
        return 'Papyrusmaking'
    elif i == 36:
        return 'Thatching'
    elif i == 37:
        return 'Gardening'
    elif i == 38:
        return 'Meditating'
    elif i == 39:
        return 'Forestry'
    elif i == 40:
        return 'Rake'
    elif i == 41:
        return 'Scythe'
    elif i == 42:
        return 'Sickle'
    elif i == 43:
        return 'Small Axe'
    elif i == 44:
        return 'Mining'
    elif i == 45:
        return 'Digging'
    elif i == 46:
        return 'Pickaxe'
    elif i == 47:
        return 'Shovel'
    elif i == 48:
        return 'Pottery'
    elif i == 49:
        return 'Ropemaking'
    elif i == 50:
        return 'Woodcutting'
    elif i == 51:
        return 'Hatchet'
    elif i == 52:
        return 'Leatherworking'
    elif i == 53:
        return 'Cloth tailoring'
    elif i == 54:
        return 'Masonry'
    elif i == 55:
        return 'Blades smithing'
    elif i == 56:
        return 'Weapon heads smithing'
    elif i == 57:
        return 'Chain armour smithing'
    elif i == 58:
        return 'Plate armour smithing'
    elif i == 59:
        return 'Shield smithing'
    elif i == 60:
        return 'Blacksmithing'
    elif i == 61:
        return 'Dairy food making'
    elif i == 62:
        return 'Hot food cooking'
    elif i == 63:
        return 'Baking'
    elif i == 64:
        return 'Beverages'
    elif i == 65:
        return 'Longsword'
    elif i == 66:
        return 'Large maul'
    elif i == 67:
        return 'Medium maul'
    elif i == 68:
        return 'Small maul'
    elif i == 69:
        return 'Warhammer'
    elif i == 70:
        return 'Long spear'
    elif i == 71:
        return 'Halberd'
    elif i == 72:
        return 'Staff'
    elif i == 73:
        return 'Carving knife'
    elif i == 74:
        return 'Butchering knife'
    elif i == 75:
        return 'Stone chisel'
    elif i == 76:
        return 'Huge club'
    elif i == 77:
        return 'Saw'
    elif i == 78:
        return 'Butchering'
    elif i == 79:
        return 'Carpentry'
    elif i == 80:
        return 'Firemaking'
    elif i == 81:
        return 'Tracking'
    elif i == 82:
        return 'Small wooden shield'
    elif i == 83:
        return 'Medium wooden shield'
    elif i == 84:
        return 'Large wooden shield'
    elif i == 85:
        return 'Small metal shield'
    elif i == 86:
        return 'Large metal shield'
    elif i == 87:
        return 'Medium metal shield'
    elif i == 88:
        return 'Large axe'
    elif i == 89:
        return 'Huge axe'
    elif i == 90:
        return 'Shortsword'
    elif i == 91:
        return 'Two handed sword'
    elif i == 92:
        return 'Hammer'
    elif i == 93:
        return 'Paving'
    elif i == 94:
        return 'Prospecting'
    elif i == 95:
        return 'Fishing'
    elif i == 96:
        return 'Locksmithing'
    elif i == 97:
        return 'Repairing'
    elif i == 98:
        return 'Coal-making'
    elif i == 99:
        return 'Milling'
    elif i == 100:
        return 'Metallurgy'
    elif i == 101:
        return 'Natural substances'
    elif i == 102:
        return 'Jewelry smithing'
    elif i == 103:
        return 'Fine carpentry'
    elif i == 104:
        return 'Bowyery'
    elif i == 105:
        return 'Fletching'
    elif i == 106:
        return 'Yoyo'
    elif i == 107:
        return 'Puppeteering'
    elif i == 108:
        return 'Toy making'
    elif i == 109:
        return 'Weaponless fighting'
    elif i == 110:
        return 'Aggressive fighting'
    elif i == 111:
        return 'Defensive fighting'
    elif i == 112:
        return 'Normal fighting'
    elif i == 113:
        return 'First aid'
    elif i == 114:
        return 'Taunting'
    elif i == 115:
        return 'Shield bashing'
    elif i == 116:
        return 'Milking'
    elif i == 117:
        return 'Preaching'
    elif i == 118:
        return 'Prayer'
    elif i == 119:
        return 'Channeling'
    elif i == 120:
        return 'Exorcism'
    elif i == 121:
        return 'Archaeology'
    elif i == 122:
        return 'Foraging'
    elif i == 123:
        return 'Botanizing'
    elif i == 124:
        return 'Climbing'
    elif i == 125:
        return 'Stone cutting'
    elif i == 126:
        return 'Lock picking'
    elif i == 127:
        return 'Stealing'
    elif i == 128:
        return 'Traps'
    elif i == 129:
        return 'Catapults'
    elif i == 130:
        return 'Animal taming'
    elif i == 131:
        return 'Animal husbandry'
    elif i == 132:
        return 'Short bow'
    elif i == 133:
        return 'Long bow'
    elif i == 134:
        return 'Medium bow'
    elif i == 135:
        return 'Ship building'
    elif i == 136:
        return 'Cartography'
    elif i == 137:
        return 'Trebuchets'
    elif i == 138:
        return 'Restoration'

json_data_type = NewType("json_data_type", List[Dict[str, List]])

def get_instructions()-> List:
    filepath_json = Path.cwd() / f"instructions.json"
    json_data = json_data_type(None)
    if filepath_json.exists():
        with filepath_json.open("r", encoding="utf-8") as f:
            try:
                 json_data =  json_data_type(jload(f))
            except JSONDecodeError:
                pass
    sim_list = []
    name = ""
    for i in json_data:
        for k, v in i.items():
            if k == "recipe_name":
                name = v
            if k == "toon_offset":
                sim_list.append([["toon offset", v]])
            elif k == "cooker":
                sim_list.append(Cooker.get_cookers(v))
            elif k == "container":
                sim_list.append(Container.get_container(v))
            elif k == "ingredients":
                sim_list.append(Ingredients.get_ingredient(v))
            else:
                #TODO error codes to convey an unrecognized group name.
                pass
    return sim_list, name
        
def get_previous_rec(name:str) -> np.ndarray:
    matches = np.zeros([], dtype=[("index", "i2"), ("desc", "U1024")])
    filepathJson = Path.cwd() / name / f"{name}.json"
    if filepathJson.exists():
        with filepathJson.open("r", encoding="utf-8") as f:
            try:
                matches = np.array(json.loads(f.read(), object_hook=decode_recipes), dtype=[("index", "i2"), ("desc", "U1024")])
            except JSONDecodeError:
                pass
    else:
        if (not Path(Path.cwd() / name).exists() or
                not Path(Path.cwd() / name).is_dir()):
            Path(Path.cwd() / name).mkdir()
        #matches = np.array()
        c = list((x+1, " ") for x in range(138))
        matches = np.array(c, dtype=[("index", "i2"), ("desc", "U1024")])
    return matches

def gen_numpy_slices(total_size:int, sim_list:list, group_size:int) -> np.ndarray:
    _gen = (v for v in it_product(*sim_list))
    #indexes = np.zeros([min(group_size, total_size)], dtype="i2")
    #recipes = np.zeros([min(group_size, total_size)], dtype="U1024")
    complex_rec = np.zeros([min(group_size, total_size)], dtype=[("index", "i2"), ("desc", "U1024")])
    
    end: int = min(group_size, total_size) - 1
    key_adj: int = 0
    for k, v in enumerate(_gen):
        k: int
        v: list
        a = np.array(v, dtype=object)
        index: int = (a[:, 1:].flatten().sum() % 138) + 1
        rec: str = ', '.join(list(map(str, a.flatten())))
        #indexes[k - key_adj] = index
        #recipes[k - key_adj] = rec
        complex_rec[k - key_adj] = (index, rec)
        if k == end:
            end = k + min(group_size, total_size - k - 1)
            key_adj = k + 1
            #yield [indexes, recipes]
            indices: np.ndarray = complex_rec['index']
            _, u_indices = np.unique(indices, return_index=True)  # unique doesn't work with mixed data arrays
            ret: np.ndarray = complex_rec[u_indices]
            yield ret
            #indexes = np.empty([min(group_size, total_size - k)], dtype="i4")
            #recipes = np.empty([min(group_size, total_size - k)], dtype="U1024")
            complex_rec = np.zeros([min(group_size, total_size - k)], dtype=[("index", "i2"), ("desc", "U1024")])

def encode_recipes(r: np.ndarray) -> dict:
    if isinstance(r, np.ndarray) and r.dtype == np.dtype([('index', '<i2'), ('desc', '<U1024')]):
        rec: np.ndarray
        _l = []
        for rec in np.nditer(r):
            _l.append({'__recipe__':True, 'index': int(rec['index']), 'desc': str(rec['desc'])})
        return _l
    else:
        type_name = r.__class__.__name__
        raise TypeError(f"Object of type '{type_name}' is not JSON serializable")   

def decode_recipes(r: str) -> np.ndarray:
    if '__recipe__' in r:
        return (int(r["index"]), str(r["desc"]))
    return r


if __name__ == '__main__':
    sim_list, name = get_instructions()
    json_file = Path.cwd() / name / f"{name}.json"
    recipes = get_previous_rec(name)
    total_size = 1
    for v in sim_list:
        total_size *= len(v)

    group_size = 100000
    _gen = gen_numpy_slices(total_size, sim_list, group_size=group_size)
    #recipes = np.zeros([], dtype=[("index", "i2"), ("desc", "U1024")])
    for k, v in enumerate(_gen):
        k: int
        v: np.ndarray
        recipes = np.hstack((v, recipes))
    
    indices: np.ndarray = recipes['index']
    _, u_indices = np.unique(indices, return_index=True)  # unique doesn't work with mixed data arrays
    recipes = recipes[u_indices]
    # TODO need to handle the occoational 
    #mask = np.ones(len(recipes), dtype=bool)
    #mask[[0]] = False
    #recipes = recipes[mask,...]
    encoded = encode_recipes(recipes)
    with open(json_file, mode='w', encoding="utf-8") as f:
        rec_json = json.dump(obj=recipes, fp=f, default=encode_recipes, separators=(',', ':'), indent=2)

    with open(file=Path.cwd() / name / f"{name}.csv", mode="w", encoding="utf-8") as f:
        for v in np.nditer(recipes):
            s = f"{get_skill_name(int(v['index']))}, {v['index']}, {v['desc']}\n"
            f.write(s)
