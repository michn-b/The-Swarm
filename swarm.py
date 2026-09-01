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

    def get_swarm_tree(self):
         return cKDTree(self.positions, boxsize=[parameters.L, parameters.L])

    def update_angles(self, predator):
        swarm_tree = self.get_swarm_tree()
        distances = swarm_tree.sparse_distance_matrix(swarm_tree, 
                                                max_distance = parameters.r, 
                                                output_type = 'coo_matrix')
        distances.eliminate_zeros()
        angles_with_neighbours = self.angles[distances.row]
        exp_matrix = coo_matrix((np.exp(1j * angles_with_neighbours), 
                                 (distances.row, distances.col)), 
                                 shape = (parameters.N, parameters.N))
        sum_exp = np.array(exp_matrix.sum(axis = 0)).flatten()
        swarm_random_angles = (np.random.rand(parameters.N) - 0.5) * 2 * np.pi
        self.angles = (np.angle(sum_exp) + parameters.a * swarm_random_angles)

        birds_nearby_predator = swarm_tree.query_ball_point(predator.position, parameters.r_p)
        vectors_to_birds = np.remainder(self.positions[birds_nearby_predator] - predator.position 
                                     + parameters.L/2, parameters.L) - parameters.L/2
        new_angles = np.arctan2(vectors_to_birds[:, 1], vectors_to_birds[:, 0])
        birds_random_angles = ((np.random.random(len(birds_nearby_predator)) - 0.5) * 2 * np.pi)
        self.angles[birds_nearby_predator] = new_angles + parameters.a * birds_random_angles

    def update_positions(self):
        self.positions[:, 0] = self.positions[:, 0] + parameters.v_0 * np.cos(self.angles) * parameters.dt
        self.positions[:, 1] = self.positions[:, 1] + parameters.v_0 * np.sin(self.angles) * parameters.dt
        self.positions = self.positions % parameters.L
