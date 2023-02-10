import itertools as it
import json
import pathlib
import concurrent.futures
from dataclasses import dataclass
from typing import Generator
from multiprocessing import Lock
from collections import namedtuple


@dataclass
class Skills:
    id: int
    name: str

    @staticmethod
    def populate(file_name):
        filepath_json = pathlib.Path.cwd() / f"{file_name}"
        json_data = {}
        if filepath_json.exists():
            with filepath_json.open("r", encoding="utf-8") as f:
                try:
                    json_data = json.load(f)
                except json.JSONDecodeError:
                    pass
            _skills = []
            for i in json_data:
                _skills.append(Skills(int(i["id"]), i["name"]))
            return _skills
        else:
            with filepath_json. open("w", encoding="utf-8"):
                pass
            return []


skills = Skills.populate("skills.json")


def get_skill_name(_id):
    for v in skills:
        if v.id == _id:
            return v.name


@dataclass
class FoodStates:
    name: str
    modifier: int

    @staticmethod
    def populate(file_name):
        filepath_json = pathlib.Path.cwd() / f"{file_name}"
        json_data = {}
        if filepath_json.exists():
            with filepath_json.open("r", encoding="utf-8") as f:
                try:
                    json_data = json.load(f)
                except json.JSONDecodeError:
                    pass
            _states = []
            for i in json_data:
                _states.append(Skills(i["name"], i["modifier"]))
            return _states
        else:
            with filepath_json. open("w", encoding="utf-8"):
                pass
            return []


rec_gen_val = namedtuple("rec_gen_val", ["gen", "rec"])

def _rec_iter(x:rec_gen_val):
    for recipe in x.gen:
        _sum = 0
        for ingredient in recipe:
            _sum = _sum + ingredient[1]
        affinity_num = (_sum % 138) + 1
        _aff = str(affinity_num)
        _rec_len = len(recipe)
        with x.rec._lock:
            if _aff in x.rec.matches.keys():
                continue
            if _rec_len > x.rec.recipe_length:
                x.rec.recipe_length = len(recipe)
            x.rec.matches[str(affinity_num)] = recipe
            print(f"Size:{len(x.rec.matches.keys())}   {x.rec.matches.keys()}")
            if len(x.rec.matches.keys()) == 138:
                return

class Recipe:
    # init method or constructor
    def __init__(self, file_name):
        self.fileName = file_name
        self.filepathJson = pathlib.Path.cwd() / self.fileName / f"{self.fileName}.json"
        self.matches = {}
        self.match_recipes = []
        self._lock = Lock()
        if self.filepathJson.exists():
            with self.filepathJson.open("r", encoding="utf-8") as f:
                try:
                    self.matches = json.load(f)
                except json.JSONDecodeError:
                    pass

        else:
            if (not pathlib.Path(pathlib.Path.cwd() / self.fileName).exists() or
                    not pathlib.Path(pathlib.Path.cwd() / self.fileName).is_dir()):
                pathlib.Path(pathlib.Path.cwd() / self.fileName).mkdir()

        self.recipe_length = 0
        for values in self.matches.values():
            if len(values) > self.recipe_length:
                self.recipe_length = len(values)
    
    def simulate(self, ingredients: list):
        rec_combo = (e for e in it.product(*ingredients))
        # simulated_recipes = list(it.product(*ingredients))
        _values = rec_gen_val(gen=(e for e in it.product(*ingredients)), rec=self)
        
        #_rec_iter(_values)
        #print(_values)
        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(_rec_iter, _values) 
                
        with self.filepathJson.open("w", encoding="utf-8") as f:
            json.dump(self.matches, f)

        filepath_csv = pathlib.Path.cwd() / self.fileName / f"{self.fileName}.csv"
        with filepath_csv.open("w", encoding="utf-8") as f:
            for index in range(1, 139):
                if str(index) not in self.matches.keys():
                    f.write(f"{get_skill_name(index)}, {index}\n")
                else:
                    v = self.matches[str(index)]
                    csv_str = ""
                    for value in v:
                        csv_str = csv_str + f"{value[0]}, {value[1]}, "
                    csv_str = csv_str + f"{get_skill_name(index)}, {index}\n"
                    f.write(csv_str)

    def get_options_affinity(self, ingredients, affinity_num):
        simulated_recipes = list(it.product(*ingredients))
        for recipe in simulated_recipes:
            ingredient_sum = 0
            for ingredient in recipe:
                ingredient_sum = ingredient_sum + ingredient[1]

            _affinity_num = (ingredient_sum % 138) + 1
            if _affinity_num != affinity_num:
                continue
            self.match_recipes.append(recipe)
        filepath_match = (pathlib.Path.cwd() / self.fileName /
                          f"{get_skill_name(affinity_num)}_{affinity_num}.csv")
        with filepath_match.open("w", encoding="utf-8") as f:
            v = self.match_recipes
            csv_str = ""
            for value in v:
                csv_str = csv_str + f"{value[0]}, {value[1]}, "
            csv_str = csv_str + f"\n"
            f.write(csv_str)


def unfermented_moonshine():
    toon = [["joe", 87]]
    # [["Ogare", 92]]
    cookers = [["oven", 178], ["rare oven", 179]]
    containers = [["cauldron", 351]]
    water = [["water", 6], ["salt water", 16]]
    sugar = [["sugar", 47]]
    grain = [["wheat", 25], ["barley", 23], ["oat", 25], ["rye", 23]]
    wheat = [["wheat", 25]]
    barley = [["barley", 23]]
    oat = [["oat", 25]]
    rye = [["rye", 23]]
    pea = [["roasted pea", 62], ["fried pea", 59]]
    corn = [["roasted corn", 48], ["fried corn", 45]]
    garlic = [["roasted garlic", 96], ["fried garlic", 93]]
    tomato = [["roasted tomato", 47], ["fried tomato", 44]]
    pea_pods = [["roasted pea pods", 50], ["fried pea pods", 47]]
    carrot = [["roasted carrot", 45], ["fried carrot", 42]]
    cucumber = [["roasted cucumber", 21], ["fried cucumber", 18]]
    onion = [["roasted onion", 95], ["fried onion", 92]]
    potato = [["roasted potato", 51], ["fried potato", 48]]
    lettuce = [["roasted lettuce", 49], ["fried lettuce", 46]]
    pumpkin = [["roasted pumpkin", 49], ["fried pumpkin", 46]]
    cabbage = [["roasted cabbage", 46], ["fried cabbage", 43]]

    weight = [["roasted pumpkin", 49], ["fried pumpkin", 46], ["roasted cabbage", 46], ["fried cabbage", 43]]
    
    ingredients = [toon, cookers, containers, water, sugar, wheat, 
                    barley, oat, rye, pea, corn, garlic, tomato, 
                    pea_pods, carrot, cucumber, onion, potato, lettuce, pumpkin, 
                    cabbage, weight, weight, weight, weight, weight, weight,
                    weight, weight, weight, weight, weight, weight, 
                    weight]
    unf_moonshine_recipes = Recipe("unf moonshine")
    unf_moonshine_recipes.simulate(ingredients)


def herb_tea():
    toon = [["Ogare", 92]]
    cookers = [["oven", 178], ["campfire", 37]]
    containers = [["pottery bowl", 77], ["cauldron", 351]]
    water = [["salt water", 16], ["water", 6]]
    tea_herbs = [["chopped lovage", 105], ["chopped rosemary", 115],
                 ["chopped basil", 111], ["chopped belladonna", 113],
                 ["chopped mint", 54], ["chopped oregano", 109],
                 ["chopped parsley", 110], ["chopped sage", 106],
                 ["chopped thyme", 112], ["chopped fennel plant", 56],
                 ["chopped camellia", 36]]
    # ["chopped sassafras", 118], ["chopped nettles", 117],
    sweet = [["sugar", 47], ["honey", 89], ["maple syrup", 17]]
    sour_savory = [["lemon juice", 25], ["cow milk", 22], ["sheep milk", 64],
                   ["bison milk", 65]]
    ingredients = [toon, cookers, containers, water, tea_herbs, sweet,
                   sour_savory]
    herb_tea_recipes = Recipe("herb tea")
    herb_tea_recipes.simulate(ingredients)


def breakfast():
    toon = [["Ogare", 92]]
    container = [["pottery bowl", 77]]
    cooker = [["oven", 178]]

    pea = [["roasted pea", 62], ["fried pea", 59]]  # 1150  58
    corn = [["roasted corn", 48], ["fried corn", 45]]  # 32   44
    garlic = [["roasted garlic", 96], ["fried garlic", 93]]  # 356
    tomato = [["roasted tomato", 47], ["fried tomato", 44]]  # 1135   43
    pea_pods = [["roasted pea pods", 50], ["fried pea pods", 47]]  # 1138  46
    carrot = [["roasted carrot", 45], ["fried carrot", 42]]  # 1133   41
    cucumber = [["roasted cucumber", 21], ["fried cucumber", 18]]  # 1247  17
    onion = [["roasted onion", 95], ["fried onion", 92]]  # 355   91
    potato = [["roasted potato", 51], ["fried potato", 48]]  # 35  47
    lettuce = [["roasted lettuce", 49], ["fried lettuce", 46]]  # 1137  45
    pumpkin = [["roasted pumpkin", 49], ["fried pumpkin", 46]]  # 33   45
    cabbage = [["roasted cabbage", 46], ["fried cabbage", 43]]  # 1134   42

    meat = [["fried meat, bear", 17], ["fried meat, canine", 19],
            ["fried meat, feline", 20], ["fried meat, game", 23],
            ["fried meat, horse", 24], ["fried meat, human", 25],
            ["fried meat, humanoid", 26], ["fried meat, insect", 27]]

    cheeses = [["feta cheese", 86]]

    ketchup = [["ketchup", 119]]

    cooked_fries = [["cooked_fries", 118]]

    lovage = [["chopped lovage", 105], ["lovage", 89]]  # 353
    rosemary = [["chopped rosemary", 115], ["rosemary", 99]]  # 363
    basil = [["chopped basil", 111], ["basil", 95]]  # 359
    belladonna = [["chopped belladonna", 113], ["belladonna", 97]]  # 361
    mint = [["chopped mint", 54], ["mint", 38]]  # 1130
    oregano = [["chopped oregano", 109], ["oregano", 93]]  # 357
    parsley = [["chopped parsley", 110], ["parsley", 94]]  # 358
    sage = [["chopped sage", 106], ["sage", 90]]  # 354
    thyme = [["chopped thyme", 112], ["thyme", 96]]  # 360
    fennel_plant = [["chopped fennel plant", 56], ["fennel plant", 40]]  # 1132
    herbs = (lovage, rosemary, basil, belladonna, mint, oregano,
             parsley, sage, thyme, fennel_plant)

    fennel_seed = [["ground fennel seed", 75], ["fennel seed", 59]]  # 1151
    cumin = [["ground cumin", 64], ["cumin", 48]]  # 1140
    paprika = [["ground paprika", 67], ["paprika", 51]]  # 1143
    turmeric = [["ground turmeric", 68], ["turmeric", 52]]  # 1144
    ginger = [["ground ginger", 65], ["ginger", 49]]  # 1141
    spices = (fennel_seed, cumin, paprika, turmeric, ginger)

    herb_spice = (*herbs, *spices)
    herb_sample = []
    herb_groups = list(it.combinations_with_replacement(
        (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14), 2))
    breakfast_recipes = Recipe("breakfast")
    for herb_indexes in herb_groups:
        ingredients = [toon, container, cooker, pea, corn, garlic, tomato, 
                        pea_pods, carrot, cucumber, onion, potato, lettuce, 
                        pumpkin, cabbage, cheeses, ketchup, cooked_fries]
        for index in herb_indexes:
            ingredients.append(herb_spice[index])
        breakfast_recipes.simulate(ingredients)

    return


def salad():
    toon = [["Ogare", 92]]
    container = [["plate", 69]]
    lettuce = [["roasted lettuce", 49], ["fried lettuce", 46]]
    meat = [["fried meat bear", 17], ["fried meat canine", 19],
            ["fried meat feline", 20], ["fried meat game", 23],
            ["fried meat horse", 24], ["fried meat human", 25],
            ["fried meat humanoid", 26], ["fried meat insect", 27],
            ["roasted meat bear", 20], ["roasted meat canine", 22],
            ["roasted meat feline", 23], ["roasted meat game", 26],
            ["roasted meat horse", 27], ["roasted meat human", 28],
            ["roasted meat humanoid", 29], ["roasted meat insect", 30]]

    mushroom = []
    corn = [["mashed corn", 76], ["chopped corn", 60]]  # 44
    onion = [["mashed onion", 123], ["chopped onion", 107]]  # 91
    potato = [["mashed potato", 79], ["chopped potato", 63]]  # 47
    cabbage = [["mashed cabbage", 74], ["chopped cabbage", 58]]  # 42
    carrot = [["mashed carrot", 73], ["chopped carrot", 57]]  # 41
    pea = [["mashed pea", 90], ["chopped pea", 74]]  # 58
    pea_pods = [["mashed pea pods", 78], ["chopped pea pods", 62]]  # 46
    tomato = [["roasted tomato", 75], ["fried tomato", 59]]  # 43
    cucumber = [["roasted cucumber", 49], ["fried cucumber", 33]]  # 17
    salad_recipes = Recipe("salad")
    ingredients = [toon, container, lettuce, meat, corn, onion, potato, cabbage,
                   carrot, pea, pea_pods, tomato, cucumber]
    salad_recipes.simulate(ingredients)


if __name__ == '__main__':
    unfermented_moonshine()
