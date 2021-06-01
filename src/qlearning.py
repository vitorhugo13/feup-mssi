import os
import sys
import numpy as np

# Table representation 

#                   Car utility |    Bus utility
#  Start point          23                 30

# each agent will have its own table
STATE_SIZE = 1
ACTION_SIZE = 2

# initialize our Q-table
QLEARNING_TABLE = np.zeros((STATE_SIZE, ACTION_SIZE))

# choose action that agent will choose
def choose_action():
    max_utility = np.argmax(QLEARNING_TABLE, axis=1)
    return max_utility

# update table using some qlearning equation
def update_table(index, value):
    QLEARNING_TABLE[0, index] = value
    return

# entry point
def main():
    print(QLEARNING_TABLE)
    
    print(choose_action())
    update_table(1,50)
    print(choose_action())
    update_table(0,90)
    print(choose_action())

    print(QLEARNING_TABLE)

    return

if __name__ == '__main__':
    main()

