"""
Module with Q-learning

Classes:
    Qlearning
"""
import environment as ev
from agent import Agent


class Qlearning:
    @staticmethod
    def learn_strategy(
        agent: Agent,
        discount_factor: float,
        learning_rate: float,
        epochs: int,
        max_steps: int
    ) -> None:
        """
        Perform Q-learning
        :param agent: agent performing action
        :param discount_factor: discount factor for future rewards
        :param learning_rate: rate at which strategy should learn
        :param epochs: number of training iterations
        :param max_steps: maximum steps that agent can perform in iteration
        """
        avg_rewards_progress = []
        for i in range(epochs):
            # Maximum number of steps
            steps = max_steps
            # Starting position for iteration
            pos_x, pos_y = agent.get_pos()

            # While possible steps and not reached exit
            while steps > 0 and not agent.reached_exit():
                # Pick action
                action = agent.pick_action()
                # Perform action and get new location
                next_x, next_y = agent.get_new_position(action)

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
                pos_x, pos_y = agent.get_pos()
            
            # Find new starting position
            agent.set_new_start_position()

            # Save q-values every 50 iterations
            if (i + 1) % 50 == 0:
                avg_values = [[round(sum(values)/4) for values in row[:-1]] for row in ev.q_values[:-1]]
                avg_rewards_progress.append(avg_values)
                print("Iteration:", i + 1)
                for row in avg_values:
                    print("".join(str(val).rjust(5) for val in row))
        return avg_rewards_progress
