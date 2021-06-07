import os
import sys
import numpy as np
import random

STATE_SIZE = 1
ACTION_SIZE = 2

class Person:
    

    def __init__(self, name):
        self.name = name
        self.QLEARNING_TABLE = np.zeros((STATE_SIZE, ACTION_SIZE))
        self.LEARNING_RATE = 0.8
        self.DISCOUNT_RATE = 0.8

        self.EXPLORATION_RATE = 0.7
        self.N = 0
    
    def my_attributes(self):
        print(self.name)
        return

    def choose_action(self):
        self.last_chosen = self.choose_action_bandit(self.QLEARNING_TABLE)
        return self.last_chosen
    
    # Index (action chosen by the user)
    # 0 = private transportation
    # 1 = public transportation

    def update_values(self, value):
        self.QLEARNING_TABLE = self.update_table(self.QLEARNING_TABLE, self.last_chosen, value)
        return 
    
    def set_vehicle(self, vehicle_name):
        self.vehicle = vehicle_name
    
    # needed to update q-table
    def increment(self):
        self.N += 1
        return self.N 

    # multiplicative function
    # decrease exploration rate as time goes by
    def update_exploration_rate(self):

        if self.N % 20 == 0:
            self.EXPLORATION_RATE = self.EXPLORATION_RATE * 0.75

        return self.EXPLORATION_RATE

    # Bellman Equation Explanation (https://towardsdatascience.com/a-beginners-guide-to-q-learning-c3e2a30a653c)
    def bellman_equation(self, index, utility, table):
        max_utility = self.choose_action_bellman(table)
        return table[0, index] + self.LEARNING_RATE*(utility + self.DISCOUNT_RATE*( table[0,max_utility] - table[0, index]))

    # index = action performed by the agent
    def bandit_algorithm(self, index, reward, table):
        self.increment()
        self.update_exploration_rate()
        return table[0, index] + (1/self.N)*(reward - table[0, index])

    # choose action that agent will choose (max_utility)
    def choose_action_bellman(self, table):
        max_utility = np.argmax(table, axis=1)
        return max_utility

    # return 0 ou 1 randomly
    def random_action_selection(self):
        random_value = random.uniform(0, 1)

        if(random_value <= 0.5):
            return 0
        else:
            return 1

    # choose action that agent will choose (Exploration vs Exploitation trade-off)
    def choose_action_bandit(self, table):
        random_value = random.uniform(0, 1)

        if(random_value <= self.EXPLORATION_RATE):
            return self.random_action_selection()
        else:
            return np.argmax(table, axis=1)[0]


    # update table using some qlearning equation
    def update_table(self, table, index, value):
        # QLEARNING_TABLE[0, index] = bellman_equation(index, value)
        table[0, index] = self.bandit_algorithm(index, value, table)
        return table


