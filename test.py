import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib.animation as animation
from Point import Point
from MathewParticleFilter import MathewParticleFilter
from BallData import BallData

filter = MathewParticleFilter(9, 6)
filter.add(BallData(0, 0, 1))
filter.update()
result = filter.getEstimate()
basepoints = filter.get_basepoints()
particles = filter.get_particles()
score = filter.evaluate_point(Point(-4, -1))
print(score)
print(basepoints)

print(Point(1, 1).angle())
print(Point(-1, 2).angle())
print(Point(-1, -4).angle())
print(Point(0, -1).angle())



test_plot = plt.scatter([p.x for p in basepoints[0]], [p.y for p in basepoints[0]], marker='x', s=20)
plt.scatter([p.x for p in particles], [p.y for p in particles], marker='o', s=5)
plt.scatter([0], [0], marker='d', s=25)
plt.show()

# num = 200
# test1 = np.random.normal(3.0, 0.1, num)
# test2 = []
# for i in range(num):
#     test2.append(np.random.normal(3.0, 0.1))
#
#
# print("max array {}, max singular {}\nmin array {}, min singular {}".format(max(test1), max(test2), min(math.fabs(x) for x in test1), min([math.fabs(x) for x in test2])))


# tmp_list = [np.random.randint(-1000, 1000) for x in range(100)]
# num_items = int(10)
# if num_items <= 0:
#     num_items = 1
#
# # saves the top percentage of particles as new basepoints
# basepoints = []
# for i in range(num_items):
#     particle = tmp_list[tmp_list.index(max(tmp_list))]
#     tmp_list.remove(max(tmp_list))
#     basepoints.append(particle)
#
# print(tmp_list)
# print(basepoints)

# test = Point(4, 5)
# # print(test)
# test.x = 100
# test.y = -823
# # print(test)
# particles = [Point(0, 0), Point(1, 1), Point(2, 2), Point(3, 3), Point (4, 4)]
#
# print(math.pi)
#
# NUM_PARTICLES = 20
# LEN_BASE= 3
#
# for i in range(NUM_PARTICLES):
#     print(int(i / (NUM_PARTICLES / LEN_BASE)))

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