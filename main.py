from word_generator import World
from environment import A_Star
from actor import Actor
import json


if __name__ == "__main__":
    with open("test_config.json", "r", encoding="utf-8") as file:
        tests = json.load(file)

    test = tests[0]
    world = World(test["border_size"], test["wall_density"])
    world.print_world()
    
    actor = Actor(world)
    print(actor.get_pos())

    A_Star.run_algorithm(actor, world)