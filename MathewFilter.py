from Point import Point
from BallData import BallData
from Ball import Ball
import math
from collections import deque
import Util
import numpy as np

# import BallFilterSimulator

MAX_BALL_SPEED = 8
NUM_PARTICLES = 100
NUM_CONDENSATIONS = 5
MAX_SPREAD = 4 # how far from a point a particle can be generated
DETECTION_WEIGHT = 100
PREDICTION_WEIGHT = 70
TOP_PERCENTAGE_OF_POINTS = 0.1


class MathewFilter:
    def __init__(self, length, width):
        self.length = length
        self.width = width

        self.particles = [None] * NUM_PARTICLES
        self.particle_confidences = [0] * NUM_PARTICLES
        self.detections = []

        self.ball = None
        self.prediction = Point(0, 0)

    def add(self, data):
        self.detections.append(data.position())

    # TODO: MAX_RANGE decreases with number of condensations???

    def getEstimate(self):
        if self.ball is None:
            return Point(0, 0)
        else:
            return self.ball

    # populates the list of particles. If no base points are given distributes particles
    # randomly aroun the field otherwise puts them around the base points
    def generate_particles(self, base_points):
        self.particles.clear()
        if len(base_points) > 0:
            # generate around points given in base_points
            for i in range(NUM_PARTICLES):
                bp = base_points[int(i / (NUM_PARTICLES / len(base_points)))]
                angle = np.random.random() * 2 * math.pi
                length = np.random.random() * MAX_SPREAD
                particle = (Point.from_angle(angle, length)).add(bp)
                self.particles.append(particle)
            assert len(self.particles) == NUM_PARTICLES
        else:
            # generate particles all over the field
            for i in range(NUM_PARTICLES):
                x = np.random.random() * self.length - self.length / 2
                y = np.random.random() * self.width - self.width / 2
                self.particles.append(Point(x, y))
            assert len(self.particles) == NUM_PARTICLES

    def update(self):
        # if there are no detections, do nothing for now
        if len(self.detections) > 0:
            basepoints = self.detections
            if self.ball is not None:
                basepoints.append(self.ball)

            for i in range(NUM_CONDENSATIONS):
                self.generate_particles(basepoints)
                self.update_particle_confidences()

                # copies the confidence list and calculates how many particles
                # we want to keep
                tmp_list = self.particle_confidences[:] # copy the list
                num_items = int(TOP_PERCENTAGE_OF_POINTS * NUM_PARTICLES)
                if num_items <= 0:
                    num_items = 1

                # saves the top percentage of particles as new basepoints
                basepoints.clear()
                for i in range(num_items):
                    particle = self.particles[tmp_list.index(max(tmp_list))]
                    tmp_list.remove(max(tmp_list))
                    basepoints.append(particle)

            # finally, take the particle with the highest confidence and use it as the ball
            self.ball = self.particles[self.particle_confidences.index(max(self.particle_confidences))]
            self.detections.clear() # clear detections for next tick

    def update_particle_confidences(self):
        for i in range(NUM_PARTICLES):
            particle = self.particles[i]
            self.particle_confidences[i] = self.evaluate_point(particle)

    def evaluate_point(self, point):
        detection_score = 0
        for d in self.detections:
            detection_dist = (d.sub(point)).length()
            # score drops to 0 at about 2m
            detection_score += DETECTION_WEIGHT * math.pow(math.e, -5 * detection_dist)

        total_score = 0
        total_score += detection_score

        return total_score


