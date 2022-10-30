"""
NOTE: You are only allowed to edit this file between the lines that say:
    # START EDITING HERE
    # END EDITING HERE

This file contains the base Algorithm class that all algorithms should inherit
from. Here are the method details:
    - __init__(self, num_arms, horizon): This method is called when the class
        is instantiated. Here, you can add any other member variables that you
        need in your algorithm.
    
    - give_pull(self): This method is called when the algorithm needs to
        select an arm to pull. The method should return the index of the arm
        that it wants to pull (0-indexed).
    
    - get_reward(self, arm_index, reward): This method is called just after the 
        give_pull method. The method should update the algorithm's internal
        state based on the arm that was pulled and the reward that was received.
        (The value of arm_index is the same as the one returned by give_pull.)

We have implemented the epsilon-greedy algorithm for you. You can use it as a
reference for implementing your own algorithms.
"""

from re import M
import numpy as np
import math
np.random.seed(0)
# Hint: math.log is much faster than np.log for scalars

class Algorithm:
    def __init__(self, num_arms, horizon):
        self.num_arms = num_arms
        self.horizon = horizon
    
    def give_pull(self):
        raise NotImplementedError
    
    def get_reward(self, arm_index, reward):
        raise NotImplementedError

# Example implementation of Epsilon Greedy algorithm
class Eps_Greedy(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # Extra member variables to keep track of the state
        self.eps = 0.1
        self.counts = np.zeros(num_arms)
        self.values = np.zeros(num_arms)
    
    def give_pull(self):
        if np.random.random() < self.eps:
            return np.random.randint(self.num_arms)
        else:
            return np.argmax(self.values)
    
    def get_reward(self, arm_index, reward):
        self.counts[arm_index] += 1
        n = self.counts[arm_index]
        value = self.values[arm_index]
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm_index] = new_value


# START EDITING HERE
# You can use this space to define any helper functions that you need
def KL(x, y):
    a = x*math.log(x/y+1e-9)
    return a + (1-x)*math.log((1-x)/(1-y)+1e-9)
# END EDITING HERE

class UCB(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # You can add any other variables you need here
        # START EDITING HERE
        self.time = 1
        self.counts = np.ones(num_arms)
        self.values = np.zeros(num_arms)
        self.ucb = np.zeros(num_arms)
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        self.time += 1
        return np.argmax(self.ucb)
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        self.counts[arm_index] += 1
        n = self.counts[arm_index]
        value = self.values[arm_index]
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm_index] = new_value
        self.ucb = self.values + np.sqrt(2*math.log(self.time)*np.reciprocal(self.counts))
        # END EDITING HERE

class KL_UCB(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # You can add any other variables you need here
        # START EDITING HERE
        self.time = 1
        self.counts = np.ones(num_arms)
        self.values = 0.5*np.ones(num_arms)
        self.kl_ucb = np.zeros(num_arms)
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        self.time += 1
        return np.argmax(self.kl_ucb)
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        self.counts[arm_index] += 1
        n = self.counts[arm_index]
        value = self.values[arm_index]
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm_index] = new_value
        for i in range(self.num_arms):
            v = (math.log(self.time)+3*math.log(math.log(self.time)))/self.counts[i]
            if v <= 0:
                self.kl_ucb[i] = self.values[i]
            else:
                l = self.values[i]
                r = 1
                m = (l+r)/2
                x = KL(self.values[i], m)
                while abs(x-v) > 0.001:
                    if x > v:
                        r = m
                    else:
                        l = m
                    m = (l+r)/2
                    x = KL(self.values[i], m)

                self.kl_ucb[i] = m
        # END EDITING HERE


class Thompson_Sampling(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # You can add any other variables you need here
        # START EDITING HERE
        self.success = np.zeros(num_arms)
        self.fail = np.zeros(num_arms)
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        maxi = 0
        max_arm = -1
        for i in range(self.num_arms):
            c = np.random.beta(self.success[i]+1, self.fail[i]+1)
            if c > maxi:
                max_arm = i
                maxi = c

        return max_arm
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        if reward == 1:
            self.success[arm_index] += 1
        else:
            self.fail[arm_index] += 1
        # END EDITING HERE
