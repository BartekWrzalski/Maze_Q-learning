"""
Module with Agent

Classes:
    Agent
"""
from world import World
import environment as ev
import random


class Agent:
    def __init__(self, world: World, epsilon: float) -> None:
        """
        :param world: instance of world for Agent to perform actions
        :param epsilon: probability of Agent choosing best possible action (default)
        """
        self.world = world
        self.epsilon = epsilon

        self.x, self.y = self.world.get_random_position()

    def set_new_start_position(self) -> None:
        # Spawn new starting position
        self.x, self.y = self.world.get_random_position()

    def get_pos(self) -> tuple[int, int]:
        return self.x, self.y

    def pick_action(self, epsilon: float = None) -> int:
        """
        Pick next action to perform
        :param epsilon: probability of Agent choosing best possible action. If not specified, get one given in constructor
        :returns: number of action to perform
        """
        if not epsilon:
            epsilon = self.epsilon

        if random.random() < epsilon:
            q_action = ev.q_values[self.x][self.y]
            return q_action.index(max(q_action))
        else:
            return random.randint(0, 3)

    def get_new_position(self, action: int) -> tuple[int, int]:
        """
        Get new position after performing action.If Agent can move to this node, move Agent
        :param action: number of action to perform
        :returns: index of next position
        """
        if ev.actions[action] == "up":
            new_x, new_y = self.x - 1, self.y
            if self.x > 0 and self.world.peek(new_x, new_y) != "x":
                self.x -= 1

        elif ev.actions[action] == "right":
            new_x, new_y = self.x, self.y + 1
            if self.y < self.world.border - 1 and self.world.peek(new_x, new_y) != "x":
                self.y += 1

        elif ev.actions[action] == "down":
            new_x, new_y = self.x + 1, self.y
            if self.x < self.world.border - 1 and self.world.peek(new_x, new_y) != "x":
                self.x += 1

        elif ev.actions[action] == "left":
            new_x, new_y = self.x, self.y - 1
            if self.y > 0 and self.world.peek(new_x, new_y) != "x":
                self.y -= 1

        return new_x, new_y

    def get_shortest_path(self) -> list[tuple[int, int]]:
        """
        Try to find path from Agent position to exit by always performing best action (epsilon = 1)
        :returns: list of nodes visited by Agent
        """
        start_x, start_y = self.x, self.y
        shortest_path = [(self.x, self.y)]

        while (
            self.world.world[self.x][self.y] == 0
            and len(shortest_path) < self.world.border**2
        ):
            # Visit new nodes until hit exit/edge/wall or stucks in loop
            action = self.pick_action(1.0)
            self.x, self.y = self.get_new_position(action)
            shortest_path.append((self.x, self.y))

        self.x, self.y = start_x, start_y
        return shortest_path

    def reached_exit(self) -> bool:
        # True if current Agent location is one of exits
        return (self.x, self.y) in self.world.good_exits + self.world.bad_exits
