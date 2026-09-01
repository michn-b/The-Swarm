import parameters
import numpy as np
from scipy.spatial import cKDTree

class Predator:

    def __init__(self, 
                     position = np.random.rand(2) * parameters.L, 
                     angle = (np.random.rand() - 0.5) * 2 * np.pi):
            self.position = position
            self.angle = angle
    
    def get_direction(self):
        dx = np.cos(self.angle)
        dy = np. sin(self.angle)
        return dx, dy

    def update_angle(self, swarm):
        swarm_tree = swarm.get_swarm_tree()
        nearest_bird = swarm_tree.query(self.position, 1)[1]
        self.angle = swarm.angles[nearest_bird] + parameters.a_p * ((np.random.random() - 0.5) * 2 * np.pi)
    
    def update_position(self):        
        self.position[0] = self.position[0] + parameters.v_0 * np.cos(self.angle) * parameters.dt
        self.position[1] = self.position[1] + parameters.v_0 * np.sin(self.angle) * parameters.dt
        self.position = self.position % parameters.L