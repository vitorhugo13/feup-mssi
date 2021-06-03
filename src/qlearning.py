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
LEARNING_RATE = 0.8
DISCOUNT_RATE = 0.8

EXPLORATION_RATE = 0.7
N = 0


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
def bellman_equation(index, utility, table):
    max_utility = choose_action_bellman(table)
    return table[0, index] + LEARNING_RATE*(utility + DISCOUNT_RATE*( table[0,max_utility] - table[0, index]))

# index = action performed by the agent
def bandit_algorithm(index, reward, table):
    increment()
    update_exploration_rate()
    print(N)
    print(EXPLORATION_RATE)
    return table[0, index] + (1/N)*(reward - table[0, index])

# choose action that agent will choose (max_utility)
def choose_action_bellman(table):
    max_utility = np.argmax(table, axis=1)
    return max_utility

# return 0 ou 1 randomly
def random_action_selection():
    random_value = random.uniform(0, 1)

    if(random_value <= 0.5):
        return 0
    else:
        return 1

# choose action that agent will choose (Exploration vs Exploitation trade-off)
def choose_action_bandit(table):
    random_value = random.uniform(0, 1)

    if(random_value <= EXPLORATION_RATE):
        return random_action_selection()
    else:
        return np.argmax(table, axis=1)


# update table using some qlearning equation
def update_table(table, index, value):
    # QLEARNING_TABLE[0, index] = bellman_equation(index, value)
    table[0, index] = bandit_algorithm(index, value, table)
    return table


