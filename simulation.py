import parameters
from swarm import Swarm
import matplotlib.pyplot as plt
import matplotlib.animation as animation

swarm = Swarm()

dx, dy = swarm.get_directions()

plt.quiver(swarm.positions[:, 0], swarm.positions[:, 1], dx, dy , swarm.angles, cmap="turbo")


plt.show()