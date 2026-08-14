import parameters
from swarm import Swarm
import matplotlib.pyplot as plt
import matplotlib.animation as animation

swarm = Swarm()

fig = plt.figure()

dx, dy = swarm.get_directions()
quiver = plt.quiver(swarm.positions[:, 0], swarm.positions[:, 1], dx, dy , swarm.angles, cmap="turbo")

def init():
    return quiver, 

def animate(i):
    swarm.update()
    dx, dy = swarm.get_directions()
    quiver.set_offsets(swarm.positions)
    quiver.set_UVC(dx ,dy, swarm.angles)
    return quiver, 

anim = animation.FuncAnimation(fig, animate, init_func = init,
                      frames = 600, interval = 1, blit = False)

plt.show()