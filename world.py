"""
Module for generating world

Classes:
    World
"""
import random


class World:
    MIN_WALL_LEN = 4
    MAX_WALL_LEN = 100

    def __init__(self, border: int, wall_density: float) -> None:
        """
        Initialize and generate world
        :param border: length of border
        :param wall_density: percent of world covered by walls
        """
        if border < self.MIN_WALL_LEN or border > self.MAX_WALL_LEN:
            raise ValueError(border)

        self.world = [[0 for _ in range(border)] for _ in range(border)]
        self.border = border

        # positions of exits
        self.good_exits = []
        self.bad_exits = []

        self.__create_exits()
        self.__generate_walls(wall_density)

    def __create_exits(self) -> None:
        """
        Create exits (2 goods and 2 bad) and save their loaction
        Exits cannot be on the corner
        """
        i = random.randint(1, self.border - 2)
        self.world[0][i] = 1
        self.good_exits.append((0, i))

        i = random.randint(1, self.border - 2)
        self.world[i][-1] = 1
        self.good_exits.append((i, self.border - 1))

        i = random.randint(1, self.border - 2)
        self.world[i][0] = 2
        self.bad_exits.append((i, 0))

        i = random.randint(1, self.border - 2)
        self.world[-1][i] = 2
        self.bad_exits.append((self.border - 1, i))

    def __generate_walls(self, density: float) -> None:
        """
        Generate walls in world
        :param density: percent of warld covered by walls
        """
        # Set of nodes that can be turned to walls, all nodes except exits
        # and corners (in contact with 2 edge)
        nodes_can_be_wall = {
            (i, j) for i in range(0, self.border - 1) for j in range(0, self.border - 1)
        }
        nodes_can_be_wall -= {
            (0, 0),
            (0, self.border - 1),
            (self.border - 1, 0),
            (self.border - 1, self.border - 1),
            *self.good_exits,
            *self.bad_exits,
        }

        number_of_walls = self.border**2 * density
        while number_of_walls > 0 and nodes_can_be_wall:
            # Create walls as long as there is space and density below desired
            # Start new wall in random position
            (i, j) = random.choice(tuple(nodes_can_be_wall))

            # If start of wall is next to edge, make wall perpendicular
            # else face wall randomly
            in_edge = True
            if i == 0:
                vector = (1, 0)
            elif i == self.border - 1:
                vector = (-1, 0)
            elif j == 0:
                vector = (0, 1)
            elif j == self.border - 1:
                vector = (0, -1)
            else:
                in_edge = False
                vector = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

            # If start of wall is on edge and diagonally touches exit, do not create wall.
            # Prevents corner that is impossible to leave
            if in_edge and any(
                [
                    abs(i - x) == 1 and abs(j - y) == 1
                    for (x, y) in self.good_exits + self.bad_exits
                ]
            ):
                nodes_can_be_wall -= {(i, j)}
                continue

            # If wall have 2 exits or exit and edge at both ends of wall, there
            # will spaces disconnected from each other, trapping actor in one of them
            if (
                in_edge
                or self.is_in_neighbourhood(i, j, 1)
                or self.is_in_neighbourhood(i, j, 2)
            ):
                can_block_path = True
            else:
                can_block_path = False

            wall_len = random.randint(2, self.border - 2)
            wall_nodes = []
            while wall_len > 0 and (i, j) in nodes_can_be_wall:
                wall_len -= 1
                self.world[i][j] = "x"

                wall_nodes.append((i, j))
                i += vector[0]
                j += vector[1]

                if can_block_path and (
                    i in [0, self.border - 1]
                    or j in [0, self.border - 1]
                    or self.is_in_neighbourhood(i, j, 1)
                    or self.is_in_neighbourhood(i, j, 2)
                ):
                    # Make sure to avoid disconnected sapces
                    break

            # For every new wall node, remove it and all its neigbours from nodes that can become wall
            for i, j in wall_nodes:
                nodes_can_be_wall -= {
                    (i, j),
                    (i - 1, j),
                    (i, j - 1),
                    (i + 1, j),
                    (i, j + 1),
                    (i - 1, j - 1),
                    (i + 1, j - 1),
                    (i + 1, j + 1),
                    (i - 1, j + 1),
                }

    def is_in_neighbourhood(self, i: int, j: int, value: int | str) -> bool:
        """
        Check if there is values in neighbourhood of node
        :param i: row of node
        :param j: column of node
        :param value: value to compare neighbourhood
        :returns: True if node or its neighbourhood equals value
        """
        return any(
            self.world[x][y] == value
            for (x, y) in [
                (i, j),
                (i - 1, j),
                (i, j - 1),
                (i + 1, j),
                (i, j + 1),
                (i - 1, j - 1),
                (i + 1, j - 1),
                (i + 1, j + 1),
                (i - 1, j + 1),
            ]
        )

    def get_random_position(self) -> tuple[int, int]:
        """
        Return random node that is not wall o exit (empty node)
        """
        i, j = random.randint(0, self.border - 1), random.randint(0, self.border - 1)
        while self.world[i][j] != 0:
            i, j = random.randint(0, self.border - 1), random.randint(
                0, self.border - 1
            )
        return i, j

    def peek(self, row: int, column: int) -> str | int | None:
        """
        Return value of node or None
        """
        if -1 < row < len(self.world) and -1 < column < len(self.world):
            return self.world[row][column]
        return None

    def print_world(self) -> None:
        for row in self.world:
            print(*row)
