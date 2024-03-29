import json
import os
import random


def get_water_reading():
    return get_simulated_water()

def get_simulated_water():
    water = 0
    seed = 1
    if not os.path.isdir("data"):
        os.mkdir("data")

    if os.path.isfile("data/water.json"):
        with open("data/water.json", "r") as f:
            data = json.load(f)
            water = data["water"]
            seed = data["seed"]
    else:
        data = {"water":0, "seed":random.random()}
    
    water += seed * (random.random()+1) * 8
    data["water"] = water
    with open("data/water.json", "w") as f:
        json.dump(data, f)
    return water
