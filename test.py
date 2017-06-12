import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib.animation as animation
from Point import Point

test = Point(4, 5)
# print(test)
test.x = 100
test.y = -823
# print(test)
particles = [Point(0, 0), Point(1, 1), Point(2, 2), Point(3, 3), Point (4, 4)]

print(math.pi)

NUM_PARTICLES = 20
LEN_BASE= 3

for i in range(NUM_PARTICLES):
    print(int(i / (NUM_PARTICLES / LEN_BASE)))

# sum = 0
# print([sum+=d for d in range(5)])
# print([i for i in range(5)])
# for i in sorted(range(len(particles)), reverse=True):
#     if i%2 == 1:
#         print("deleting{}".format([particles[i]]))
#         del particles[i]  # delete the particle from the list
#     else:
#         print("updateing {}".format(particles[i]))

# for i in range(len(particles)):
#     # if i >= len(particles):
#     #     break
#     if i%2 == 0:
#         print("deleting {}".format([particles[i]]))
#         del particles[i]  # delete the particle from the list
#     # else:
#     #     print("updateing {}".format(particles[i]))
#         # self.particles_[i].updateVelocity(timeDelta)
        # self.particles_[i].updatePosition(timeDelta)

# print(particles)


# def main():
#     numframes = 100
#     numpoints = 10
#     color_data = np.random.random((numframes, numpoints))
#     x, y, c = np.random.random((3, numpoints))
#
#     fig = plt.figure()
#     scat = plt.scatter(x, y, c=c, s=100)
#
#     ani = animation.FuncAnimation(fig, update_plot, frames=numframes,
#                                   fargs=(color_data, scat))
#     plt.show()
#
# def update_plot(i, data, scat):
#     scat.set_array(data[i])
#     print(data[i])
#     return scat,
#
# main()