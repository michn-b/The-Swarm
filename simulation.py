import parameters
from swarm import Swarm
import numpy as np
import matplotlib.pyplot as plt

swarm = Swarm()

dx, dy = swarm.get_direction()

plt.quiver(swarm.position[:, 0], swarm.position[:, 1], dx, dy , swarm.theta, cmap="turbo")
plt.show()