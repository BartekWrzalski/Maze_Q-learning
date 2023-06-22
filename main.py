from world import World
from environment import set_default_q_values, set_rewards, print_word_after_strategy
from a_star import A_Star
from q_learning import Qlearning
from actor import Actor
import json


if __name__ == "__main__":
    with open("test_config.json", "r", encoding="utf-8") as file:
        tests = json.load(file)

    test = tests[0]
    world = World(test["border_size"], test["wall_density"])
    world.print_world()

    set_default_q_values(test["border_size"])
    set_rewards(world)
    
    actor = Actor(world, test["epsilon"])
    print(actor.get_pos())

    # A_Star.run_algorithm(actor, world)
    Qlearning.learn_strategy(actor, world, test["discount_factor"], test["learning_rate"], test["epochs"], test["m"])
    print_word_after_strategy(world)
    path = actor.get_shortest_path()
    print(" -> ".join(str(step) for step in path))
    
