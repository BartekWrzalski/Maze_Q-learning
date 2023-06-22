"""
Module with Q-learning

Classes:
    Qlearning
"""
import environment as ev
from actor import Actor
from world import World


class Qlearning:
    @staticmethod
    def learn_strategy(
        actor: Actor,
        world: World,
        discount_factor: float,
        learning_rate: float,
        epochs: int,
        step_multiplier: int,
    ) -> None:
        """
        Perform Q-learning
        :param actor: actor performing action
        :param world: world to learn strategy on
        :param discount_factor: discount factor for future rewards
        :param learning_rate: rate at which strategy should learn
        :param epochs: number of training iterations
        :param step_multiplier: steps multiplier for maximum number of performed steps
        """
        for i in range(epochs):
            # Maximum number of steps
            steps = world.border * step_multiplier
            # Starting position for iteration
            pos_x, pos_y = actor.get_pos()

            # While possible steps and not reached exit
            while steps > 0 and world.peek(pos_x, pos_y) not in [1, 2]:
                # Pick action
                action = actor.pick_action()
                # Perform action and get new location
                next_x, next_y = actor.get_new_position(action)

                # Receive reward and calculate temporal difference
                reward = ev.rewards[next_x][next_y]
                old_q_val = ev.q_values[pos_x][pos_y][action]
                temporal_difference = (
                    reward - old_q_val
                    + discount_factor * max(ev.q_values[next_x][next_y])
                )

                # Update q-value for action and node pair. Round to 2 decimal palces
                new_q_val = old_q_val + temporal_difference * learning_rate
                ev.q_values[pos_x][pos_y][action] = round(new_q_val, 2)

                steps -= 1
                pos_x, pos_y = actor.get_pos()
            
            # Find new starting position
            actor.set_new_start_position()

            # Save q-values every 50 iterations
            # if i % 20 == 0:
            #     for row in ev.q_values[:-1]:
            #     print(*row[:-1])
