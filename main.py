import json

import environment as ev
from a_star import A_Star
from agent import Agent
from environment import set_default_q_values, set_rewards
from q_learning import Qlearning
from world import World

if __name__ == "__main__":
    with open("test_config.json", "r", encoding="utf-8") as file:
        tests = json.load(file)

    for test in tests:
        world = World(test["border_size"], test["wall_density"])
        agent = Agent(world, test["epsilon"])
        world.print_world()

        set_default_q_values(test["border_size"])
        set_rewards(world)

        rewards_progress = Qlearning.learn_strategy(
            agent,
            test["discount_factor"],
            test["learning_rate"],
            test["epochs"],
            test["step_multiplier"] * test["border_size"],
        )
        q_path = agent.get_shortest_path()

        a_path = A_Star.run_algorithm(agent, world)
        print(q_path)
        print(a_path)

        with open("Results/" + test["name"] + ".txt", "w", encoding="utf-8") as file:
            for arg, value in test.items():
                file.write(f"{arg}: {value}\n")
            for row in world.world:
                file.write(" ".join(map(str, row)) + "\n")

            file.write("\nAverage q-values every 50 iterations:")
            for i, avg_val in enumerate(rewards_progress):
                file.write(f"\nIteration: {(i + 1) * 50}\n")
                for row in avg_val:
                    file.write("".join(str(val).rjust(4) for val in row) + "\n")

            file.write("\nWorld with best moves from strategy:\n")
            move_to_char = {"up": "^", "left": "<", "down": "v", "right": ">"}
            for i, row in enumerate(world.world):
                row_strategy = []
                for j, value in enumerate(row):
                    if value != 0:
                        row_strategy.append(value)
                    else:
                        q_action = ev.q_values[i][j]
                        action = q_action.index(max(q_action))
                        row_strategy.append(move_to_char[ev.actions[action]])
                file.write(" ".join(map(str, row_strategy)) + "\n")

            file.write(f"\nStarting position: {agent.get_pos()}\n")
            file.write(f"Strategy path:\n{' -> '.join(map(str, q_path))}\n")
            file.write(f"A* path:\n{' -> '.join(map(str, a_path))}\n")
