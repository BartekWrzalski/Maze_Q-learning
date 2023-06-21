"""
Module for generating world

Classes:
    World
"""
import random


class World:
    """
    Class generating worlds

    Attributes:

    Methods:

    """

    MIN_WALL_LEN = 4
    MAX_WALL_LEN = 100

    def __init__(self, n: int, p: float) -> None:
        if n < self.MIN_WALL_LEN or n > self.MAX_WALL_LEN:
            raise ValueError(n)

        self.world = [[0 for _ in range(n)] for _ in range(n)]

        self.rand = random.Random()

        self.good_exits = []
        self.bad_exits = []
        self.__create_exits(n)
        self.__generate_walls(n, p)

    def __create_exits(self, n: int) -> None:
        """
        """
        i = self.rand.randint(1, n - 2)
        self.world[0][i] = 1
        self.good_exits.append((0, i))

        i = self.rand.randint(1, n - 2)
        self.world[i][-1] = 1
        self.good_exits.append((i, n - 1))

        i = self.rand.randint(1, n - 2)
        self.world[i][0] = 2
        self.bad_exits.append((i, 0))

        i = self.rand.randint(1, n - 2)
        self.world[-1][i] = 2
        self.bad_exits.append((n - 1, i))

    def __generate_walls(self, n: int, p: float) -> None:
        cells_can_be_wall = {(i, j) for i in range(0, n - 1) for j in range(0, n - 1)}
        cells_can_be_wall -= {
            (0, 0),
            (0, n - 1),
            (n - 1, 0),
            (n - 1, n - 1),
            *self.good_exits,
            *self.bad_exits,
        }

        number_of_walls = n * n * p
        while number_of_walls > 0 and cells_can_be_wall:
            (i, j) = random.choice(tuple(cells_can_be_wall))          

            in_border = True
            if i == 0:
                vector = (1, 0)
            elif i == n - 1:
                vector = (-1, 0)
            elif j == 0:
                vector = (0, 1)
            elif j == n - 1:
                vector = (0, -1)
            else:
                in_border = False
                vector = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

            if in_border and any([abs(i-x)==1 and abs(j-y)==1 for (x, y) in self.good_exits + self.bad_exits]):
                cells_can_be_wall -= {(i,j)}
                continue

            if in_border or self.is_in_neighbourhood(i, j, 1) or self.is_in_neighbourhood(i, j, 2):
                can_block_path = True
            else:
                can_block_path = False

            max_len = random.randint(2, n - 2)
            new_wall = []
            while max_len > 0 and (i, j) in cells_can_be_wall:
                max_len -= 1
                self.world[i][j] = "x"

                new_wall.append((i, j))
                i += vector[0]
                j += vector[1]

                if can_block_path and (
                    i in [0, n-1] or j in [0, n-1]
                    or self.is_in_neighbourhood(i, j, 1)
                    or self.is_in_neighbourhood(i, j, 2)
                ):
                    break

            for i, j in new_wall:
                cells_can_be_wall -= {
                    (i, j),
                    (i - 1, j),
                    (i, j - 1),
                    (i + 1, j),
                    (i, j + 1),
                    (i - 1, j - 1),
                    (i + 1, j - 1),
                    (i + 1, j + 1),
                    (i - 1, j + 1)
                }

    def is_in_neighbourhood(self, i: int, j: int, value: int | str) -> bool:
        """
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
                (i - 1, j + 1)
        ])

    def get_random_position(self) -> None:
        """ """
        while True:
            i, j = random.randint(0, len(self.world) - 1), random.randint(
                0, len(self.world) - 1
            )
            if self.world[i][j] == 0:
                return i, j

    def peek(self, i: int, j: int) -> str | int | None:
        """ """
        if -1 < i < len(self.world) and -1 < j < len(self.world):
            return self.world[i][j]
        return None

    def print_world(self) -> None:
        for row in self.world:
            print(*row)
