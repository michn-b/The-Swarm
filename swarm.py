import parameters
import numpy as np
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix

class Swarm:

    def __init__(self, 
                 positions = np.random.rand(parameters.N, 2) * parameters.L, 
                 angles = (np.random.rand(parameters.N) - 0.5) * 2 * np.pi):
        self.positions = positions
        self.angles = angles

    def get_directions(self):
        dx = np.cos(self.angles)
        dy = np. sin(self.angles)
        return dx, dy

    def update(self):
        swarm_tree = cKDTree(self.positions, boxsize=[parameters.L, parameters.L])
        distances = swarm_tree.sparse_distance_matrix(swarm_tree, 
                                                max_distance = parameters.r, 
                                                output_type = 'coo_matrix')
        distances.eliminate_zeros()
        angles_with_neighbours = self.angles[distances.row]
        exp_matrix = coo_matrix((np.exp(1j * angles_with_neighbours), 
                                 (distances.row, distances.col)), 
                                 shape = (parameters.N, parameters.N))
        sum_exp = np.array(exp_matrix.sum(axis = 0)).flatten()
        random_angles = (np.random.rand(parameters.N)-0.5) * 2 * np.pi
        self.angles = (np.angle(sum_exp) + parameters.a * random_angles)

        self.positions[:, 0] = self.positions[:, 0] + parameters.v_0*np.cos(self.angles) * parameters.dt
        self.positions[:, 1] = self.positions[:, 1] + parameters.v_0*np.sin(self.angles) * parameters.dt
        self.positions = self.positions % parameters.L
