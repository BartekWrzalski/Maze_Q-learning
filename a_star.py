"""
"""
from actor import Actor
from word_generator import World
from queue import PriorityQueue
import math
from copy import deepcopy


class A_Star:
    """ """

    def __init__(self) -> None:
        pass

    @staticmethod
    def run_algorithm(actor: Actor, world: World) -> None:
        """ """

        def calculate_distance(i: int, j: int) -> int:
            return min(
                [abs(gate[0] - i) + abs(gate[1] - j) for gate in world.good_exits]
            )

        def visualize_path(path: dict, end_node: tuple) -> None:
            world_w_path = deepcopy(world.world)
            current = end_node
            while current in path:
                current = path[current]
                world_w_path[current[0]][current[1]] = "*"

            for line in world_w_path:
                print(*line)

        distance_travelled = {actor.get_pos(): 0}
        distance_remain = {actor.get_pos(): calculate_distance(*actor.get_pos())}
        discovered = PriorityQueue()
        discovered.put((distance_remain[actor.get_pos()], actor.get_pos()))
        path = {}

        while not discovered.empty():
            _, current = discovered.get()
            if current in world.good_exits:
                visualize_path(path, current)
                return path

            for i, j in [
                (current[0] - 1, current[1]),
                (current[0] + 1, current[1]),
                (current[0], current[1] - 1),
                (current[0], current[1] + 1),
            ]:
                if world.peek(i, j) not in [0, 1]:
                    continue

                new_distance = distance_travelled[current] + 1
                if new_distance < distance_travelled.get((i, j), math.inf):
                    path[(i, j)] = current
                    distance_travelled[(i, j)] = new_distance
                    distance_remain[(i, j)] = new_distance + calculate_distance(i, j)
                    if (_, (i, j)) not in discovered.queue:
                        discovered.put((distance_remain[(i, j)], (i, j)))
        return -1
