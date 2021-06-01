import os
import sys
import numpy as np

# Table representation 

#                   Car utility |    Bus utility
#  Start point          23                 30

# each agent will have its own table
STATE_SIZE = 1
ACTION_SIZE = 2
LEARNING_RATE = 0.8
DISCOUNT_RATE = 0.8

# initialize our Q-table
QLEARNING_TABLE = np.zeros((STATE_SIZE, ACTION_SIZE))

# Bellman Equation Explanation (https://towardsdatascience.com/a-beginners-guide-to-q-learning-c3e2a30a653c)
def bellman_equation(index, utility):
    max_utility = choose_action()
    return QLEARNING_TABLE[0, index] + LEARNING_RATE*(utility + DISCOUNT_RATE*( QLEARNING_TABLE[0,max_utility] - QLEARNING_TABLE[0, index]))

# choose action that agent will choose (max_utility)
def choose_action():
    max_utility = np.argmax(QLEARNING_TABLE, axis=1)
    return max_utility

# update table using some qlearning equation
def update_table(index, value):
    QLEARNING_TABLE[0, index] = bellman_equation(index, value)
    return

# entry point
def main():
    print(QLEARNING_TABLE)
    update_table(1,50)
    print(QLEARNING_TABLE)
    update_table(0,90)
    print(QLEARNING_TABLE)
    update_table(1,10)
    print(QLEARNING_TABLE)
    return

if __name__ == '__main__':
    main()

