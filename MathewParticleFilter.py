from Point import Point
from BallData import BallData
import math
from operator import itemgetter
import Util
import numpy as np


MAX_BALL_SPEED = 8
MIN_CONFIDENCE = 0.9

# Particle filter constants
NUM_PARTICLES = 300
NUM_CONDENSATIONS = 7
MAX_SPREAD = 0.05   # the variance of randomly generated gaussian points
TOP_PERCENTAGE_OF_POINTS = 0.05 # the percentage of points to keep each condensation

DETECTION_WEIGHT = 100  # weight of a ball detection
PREVIOUS_BALL_WEIGHT = 5   # weight of the last known ball location
PREDICTION_WEIGHT = 70  # weight of the ball's predicted location


class MathewParticleFilter:
    def __init__(self, length, width):
        self.length = length
        self.width = width

        self.particles = [[0, 0] for _ in range(NUM_PARTICLES)] # [0] will hold the point, [1] will hold the confidence
        self.detections = []    # the vision detections each tick

        self.ball = None
        self.prediction = Point(0, 0)

        self.basepoints_data = []

    def add(self, data):
        # only care about detections in the field with a high confidence
        if Util.is_within_field(data.position(), self.length, self.width) and data.confidence > MIN_CONFIDENCE:
            self.detections.append(data.position())

    def getEstimate(self):
        if self.ball is None:
            return Point(0, 0)
        else:
            return self.ball

    # populates the list of particles. If no base points are given distributes particles
    # randomly aroun the field otherwise puts them around the base points
    # TODO: MAX_SPREAD decreases with number of condensations???
    def generate_particles(self, base_points):
        if len(base_points) > 0:
            # generate around points given in base_points
            for i in range(NUM_PARTICLES):
                bp = base_points[int(i / (NUM_PARTICLES / len(base_points)))]
                newx = np.random.normal(bp.x, MAX_SPREAD)
                newy = np.random.normal(bp.y, MAX_SPREAD)
                self.particles[i][0] = Point(newx, newy)
        else:
            # generate particles all over the field
            for i in range(NUM_PARTICLES):
                x = np.random.random() * self.length - self.length / 2
                y = np.random.random() * self.width - self.width / 2
                self.particles[i][0] = Point(x, y)

    def update(self):
        # set all initial basepoints
        basepoints = self.detections
        if self.ball is not None:
            basepoints.append(self.ball)

        # Do the particle generation and condensation loop
        # - generate particles around the given basepoints
        # - update the confidences of each new particle
        # - keep the top percentage of particles and use them as the new basepoints for next loop
        for i in range(NUM_CONDENSATIONS):
            self.generate_particles(basepoints)
            self.update_particle_confidences()

            num_particles_to_keep = int(TOP_PERCENTAGE_OF_POINTS * NUM_PARTICLES)
            tmp_list = sorted(self.particles.copy(), key=itemgetter(1)) # sort by confidence
            best_particles = tmp_list[-num_particles_to_keep:]

            basepoints = [p[0] for p in best_particles]

        # self.ball = basepoints[len(basepoints) - 1]
        self.ball = Util.average_points(basepoints)

        # print("ball at {}".format(self.ball))
        self.detections.clear() # clear detections for next tick

    def update_particle_confidences(self):
        for i in range(NUM_PARTICLES):
            particle = self.particles[i][0]
            self.particles[i][1] = self.evaluate_point(particle)

    # scores the point based on:
    # - proximity to a vision detection (close is better)
    # - proximity to the last ball's location (closer is better ish)
    # - proximity to the last ball's predicted location (closer is better)
    def evaluate_point(self, point):
        detection_score = 0
        for d in self.detections:
            detection_dist = (d.sub(point)).length()
            detection_score += DETECTION_WEIGHT * math.pow(math.e, -10*detection_dist)

        previous_ball_score = 0
        if self.ball is not None:
            ball_dist = (point.sub(self.ball)).length()
            if ball_dist > 0.3: # 0.3 is slightly more than the ball can travel in 1/30 of a second at 8m/s
                previous_ball_score += 0
            else:
                previous_ball_score += PREVIOUS_BALL_WEIGHT - (PREVIOUS_BALL_WEIGHT / 0.3) * ball_dist

        return detection_score + previous_ball_score

    def get_basepoints(self):
        return self.basepoints_data

    def get_particles(self):
        return [p[0] for p in self.particles]