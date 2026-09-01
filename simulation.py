import parameters
from swarm import Swarm
from predator import Predator
import matplotlib.pyplot as plt
import matplotlib.animation as animation

swarm = Swarm()
predator = Predator()

fig = plt.figure()

swarm_dx, swarm_dy = swarm.get_directions()
swarm_quiver = plt.quiver(swarm.positions[:, 0], swarm.positions[:, 1], swarm_dx, swarm_dy, swarm.angles, cmap="turbo")
pred_dx, pred_dy = predator.get_direction()
predator_quiver = plt.quiver(predator.position[0], predator.position[1], pred_dx, pred_dy, predator.angle, cmap="turbo")

def init():
    return swarm_quiver, predator_quiver

def animate(i):
    swarm.update_angles(predator)
    predator.update_angle(swarm)
    swarm.update_positions()
    predator.update_position()

    swarm_dx, swarm_dy = swarm.get_directions()
    pred_dx, pred_dy = predator.get_direction()
    
    swarm_quiver.set_offsets(swarm.positions)
    swarm_quiver.set_UVC(swarm_dx, swarm_dy, swarm.angles)
    predator_quiver.set_offsets(predator.position)
    predator_quiver.set_UVC(pred_dx, pred_dy, predator.angle)
    return swarm_quiver, predator_quiver

anim = animation.FuncAnimation(fig, animate, init_func = init,
                      frames = 600, interval = 0.5, blit = False)

plt.show()