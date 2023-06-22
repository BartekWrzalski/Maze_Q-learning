"""
Module for storing set of actions, rewards and q-values
"""
from world import World
from copy import deepcopy


actions = ["up", "right", "down", "left"]


def set_default_q_values(border: int) -> None:
    """
    Craete default q-value for every action for every node. Adds additional row
    and column at the end, whoch is used for getting q value of node beyond the world
    border.Uses python property, that makes index -1 act as last index
    :param border: length of world border
    """
    global q_values
    q_values = [
        [[0.0 for _ in range(4)] for _ in range(border + 1)] for _ in range(border + 1)
    ]


def set_rewards(world: World) -> None:
    """
    Craete reward matrix for every node. Adds addtional row and column for
    rewards for stepping beyond the world border. Prevents IndexError. Uses
    python property, that makes index -1 act as last index
    :param world: world instance to base rewards on
    """
    global rewards
    rewards = []

    for row in world.world:
        rewards.append([])
        for cell in row:
            if cell == 1:
                rewards[-1].append(100)
            elif cell == 0:
                rewards[-1].append(0)
            elif cell == "x":
                rewards[-1].append(-100)
            elif cell == 2:
                rewards[-1].append(-200)
        rewards[-1].append(-100)
    rewards.append([-100 for _ in range(world.border)])


def print_word_after_strategy(world: World):
    move_to_char = {"up": "^", "left": "<", "down": "v", "right": ">"}
    _world = deepcopy(world.world)
    for i, row in enumerate(_world):
        for j, value in enumerate(row):
            if value == 0:
                q_action = q_values[i][j]
                action = q_action.index(max(q_action))
                direc = move_to_char[actions[action]]
                _world[i][j] = direc

    for row in _world:
        print(*row)
    print(q_values)
