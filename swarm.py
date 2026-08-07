import parameters
import numpy as np
from scipy.spatial import cKDTree

class Swarm:

    def __init__(self, 
                 position = np.random.rand(parameters.N, 2) * parameters.L, 
                 theta = (np.random.rand(parameters.N) - 0.5) * 2 * np.pi):
        self.position = position
        self.theta = theta

    def get_direction(self):
        dx = np.cos(self.theta)
        dy = np.sin(self.theta)
        return dx, dy

    #def update(self):

    