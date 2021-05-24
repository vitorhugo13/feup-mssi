import os
import sys
import numpy as np

ACTION_SIZE = 2

# initialize our Q-table
def create_table(STATE_SPACE_SIZE, ACTION_SPACE_SIZE):
    q_table = np.zeros((STATE_SPACE_SIZE, ACTION_SPACE_SIZE))
    return q_table

# choose action that agent will choose
def choose_action(table):
    print (table)
    return

# update table using some qlearning equation
def update_table():
    return

# entry point
def main():
    qlearning_table = create_table(20, ACTION_SIZE)
    choose_action(qlearning_table)
    return

if __name__ == '__main__':
    main()

