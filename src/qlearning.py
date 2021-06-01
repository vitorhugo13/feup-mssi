import os
import sys
import numpy as np
import random

# 0 = private transportation
# 1 = public transportation

# Table representation 

#                   Car utility |    Bus utility
#  Start point          23                 30

# each agent will have its own table
STATE_SIZE = 1
ACTION_SIZE = 2
LEARNING_RATE = 0.8
DISCOUNT_RATE = 0.8

EXPLORATION_RATE = 0.7
N = 0

# initialize our Q-table
QLEARNING_TABLE = np.zeros((STATE_SIZE, ACTION_SIZE))

# needed to update q-table
def increment():
    global N
    N = N + 1
    return N 

# multiplicative function
# decrease exploration rate as time goes by
def update_exploration_rate():
    global EXPLORATION_RATE

    if N % 20 == 0:
        EXPLORATION_RATE = EXPLORATION_RATE * 0.75

    return EXPLORATION_RATE

# Bellman Equation Explanation (https://towardsdatascience.com/a-beginners-guide-to-q-learning-c3e2a30a653c)
def bellman_equation(index, utility):
    max_utility = choose_action_bellman()
    return QLEARNING_TABLE[0, index] + LEARNING_RATE*(utility + DISCOUNT_RATE*( QLEARNING_TABLE[0,max_utility] - QLEARNING_TABLE[0, index]))

# index = action performed by the agent
def bandit_algorithm(index, reward):
    increment()
    update_exploration_rate()
    return QLEARNING_TABLE[0, index] + (1/N)*(reward - QLEARNING_TABLE[0, index])

# choose action that agent will choose (max_utility)
def choose_action_bellman():
    max_utility = np.argmax(QLEARNING_TABLE, axis=1)
    return max_utility

# return 0 ou 1 randomly
def random_action_selection():
    random_value = random.uniform(0, 1)

    if(random_value <= 0.5):
        return 0
    else:
        return 1

# choose action that agent will choose (Exploration vs Exploitation trade-off)
def choose_action_bandit():
    random_value = random.uniform(0, 1)

    if(random_value <= EXPLORATION_RATE):
        return random_action_selection()
    else:
        return np.argmax(QLEARNING_TABLE, axis=1)


# update table using some qlearning equation
def update_table(index, value):
    # QLEARNING_TABLE[0, index] = bellman_equation(index, value)
    QLEARNING_TABLE[0, index] = bandit_algorithm(index, value)
    return

# entry point
def main():
    return

if __name__ == '__main__':
    main()

