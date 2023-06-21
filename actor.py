"""
"""
from word_generator import World


class Actor:
    """
    """
    def __init__(self, world: World) -> None:
        self.world = world
        self.x, self.y = self.world.get_random_position()

    def get_pos(self) -> tuple[int, int]:
        """
        """
        return self.x, self.y

    def make_move(self, direction: str) -> tuple[int, int]: # type (random, e-greedy), not direction. here make decision
        if direction == "up":
            self.x -= 1
        elif direction == "down":
            self.x += 1
        elif direction == "left":
            self.y -= 1
        elif direction == "right":
            self.y += 1
        
        return self.x, self.y