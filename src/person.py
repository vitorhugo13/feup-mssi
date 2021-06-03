from qlearning import *
import os
import sys
import numpy as np

STATE_SIZE = 1
ACTION_SIZE = 2

class Person:
    
    QLEARNING_TABLE = np.zeros((STATE_SIZE, ACTION_SIZE))

    def __init__(self, name):
        self.name = name
    
    def my_attributes(self):
        print(self.name)
        return

    def choose_action(self):
        return choose_action_bandit(self.QLEARNING_TABLE)
    
    # Index (action chosen by the user)
    # 0 = private transportation
    # 1 = public transportation

    def update_values(self, index, value):
        self.QLEARNING_TABLE = update_table(self.QLEARNING_TABLE, index, value)
        print(self.QLEARNING_TABLE)
        return 
    
