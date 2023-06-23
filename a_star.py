"""
Module with A* algorithm

Classes:
    A_star
"""
import math
from queue import PriorityQueue
from agent import Agent
from world import World


class A_Star:
    @staticmethod
    def run_algorithm(agent: Agent, world: World) -> list[tuple]:
        """
        Performs A* algorithm in given instance of
        :param agent: agent to get starting position from
        :param world: world on which perfomr algorithm
        :returns: list of transition from start to finish
        """

        def calculate_distance(i: int, j: int) -> int:
            # calculate distance between given position (i, j) and good gatesa
            # return distance to closest good gate
            return min(
                [abs(gate[0] - i) + abs(gate[1] - j) for gate in world.good_exits]
            )

        def final_path(path: dict, end_node: tuple) -> list[tuple]:
            # return final path
            result = [end_node]
            current = end_node
            while current in path:
                current = path[current]
                result.insert(0, current)

            return result

        # lenght of best distance from start to key node
        distance_travelled = {agent.get_pos(): 0}

        # lenght of best possible distance from start to exit if it
        # goes by key node (travelled + distance to exit)
        best_distances = {agent.get_pos(): calculate_distance(*agent.get_pos())}

        # set of nodes to be discovered, prioritize by distance to exit
        discovered = PriorityQueue()
        discovered.put((best_distances[agent.get_pos()], agent.get_pos()))

        # all transitions made during algorithm
        path = {}

        while not discovered.empty():
            _, current = discovered.get()
            if current in world.good_exits:
                return final_path(path, current)

            for i, j in [
                (current[0] - 1, current[1]),
                (current[0] + 1, current[1]),
                (current[0], current[1] - 1),
                (current[0], current[1] + 1),
            ]:
                # for each neighbour of current node
                if world.peek(i, j) not in [0, 1]:
                    continue

                # path travelled from start to new node throught current
                new_distance = distance_travelled[current] + 1
                if new_distance < distance_travelled.get((i, j), math.inf):
                    # remember new distance if is better that remembered one
                    distance_travelled[(i, j)] = new_distance
                    best_distances[(i, j)] = new_distance + calculate_distance(i, j)
                    path[(i, j)] = current

                    if (_, (i, j)) not in discovered.queue:
                        discovered.put((best_distances[(i, j)], (i, j)))
        return -1
