from Point import Point
from BallData import BallData
from Ball import Ball
import math
from operator import itemgetter
import Util
import numpy as np

MAX_BALL_SPEED = 8.5
MIN_CONFIDENCE = 0.9

# Particle filter constants
NUM_PARTICLES = 300
NUM_CONDENSATIONS = 7
MAX_SPREAD = 0.05   # the variance of randomly generated gaussian points
TOP_PERCENTAGE_OF_POINTS = 0.1   # the percentage of points to keep each condensation

# TODO: weight vision detections within the 8ms range higher than those outsied? and have prediction weight in the middle?
CLOSE_DETECTION_WEIGHT = 100  # weight of a ball detection that's within the 8m/s distance threshold
FAR_DETECTION_WEIGHT = 80   # weight of a ball detection that's outside the 8m/s distance threshold
PREVIOUS_BALL_WEIGHT = 1   # weight of the last known ball location
PREDICTION_WEIGHT = 15  # weight of the ball's predicted location


class MathewParticleFilter:
    def __init__(self, length, width):
        self.length = length
        self.width = width

        self.particles = [[0, 0] for _ in range(NUM_PARTICLES)] # [0] will hold the point, [1] will hold the confidence
        self.detections = []    # the vision detections each tick

        self.ball = None
        self.prediction = None

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

    def update(self, timeDelta, ball_=None):
        self.prediction = ball_.position(timeDelta)

        # set all initial basepoints
        basepoints = self.detections
        if self.ball is not None:
            # basepoints.append(self.ball)
            basepoints.append(self.prediction)

        # Do the particle generation and condensation loop
        # - generate particles around the given basepoints
        # - update the confidences of each new particle
        # - keep the top percentage of particles and use them as the new basepoints for next loop
        for i in range(NUM_CONDENSATIONS):
            self.generate_particles(basepoints)
            self.update_particle_confidences(timeDelta)

            num_particles_to_keep = int(TOP_PERCENTAGE_OF_POINTS * NUM_PARTICLES)
            tmp_list = sorted(self.particles.copy(), key=itemgetter(1)) # sort by confidence
            best_particles = tmp_list[-num_particles_to_keep:]

            basepoints = [p[0] for p in best_particles]

        # TODO: also check variance of basepoints? If it's too large there are probably 2 cluster so either average the one with
        # higher confidence, or instead just take the single most confident point
        # self.ball = basepoints[len(basepoints) - 1]
        self.ball = Util.average_points(basepoints)
        # print(Util.get_points_variance(basepoints))

        # print("ball at {}".format(self.ball))
        self.detections.clear() # clear detections for next tick

    def update_particle_confidences(self, timeDelta):
        for i in range(NUM_PARTICLES):
            particle = self.particles[i][0]
            self.particles[i][1] = self.evaluate_point(particle, timeDelta)

    # scores the point based on:
    # - proximity to a vision detection (close is better)
    # - proximity to the last ball's location (closer is better ish)
    # - proximity to the last ball's predicted location (closer is better)
    def evaluate_point(self, point, timeDelta):
        ball_max_dist = MAX_BALL_SPEED * timeDelta

        detection_score = 0
        for d in self.detections:
            detection_dist = (d.sub(point)).length()
            if self.ball is None or (d.sub(self.ball)).length() <= 1:
                # the detection is resonably close to the old ball. Use full weight
                detection_score += CLOSE_DETECTION_WEIGHT * math.pow(math.e, -1 * detection_dist)
            else:
                detection_score += FAR_DETECTION_WEIGHT * math.pow(math.e, -10 * detection_dist)

        previous_ball_score = 0
        if self.ball is not None:
            ball_dist = (point.sub(self.ball)).length()
            if ball_dist > 1:
                previous_ball_score -= PREVIOUS_BALL_WEIGHT
            else:
                # this is a leanear score from PREVIOUS_BALL_WEIGHT at a dist of 0, to PREVIOUS_BALL_WEIGHT/2 at a dist of ball_max_dist
                previous_ball_score += PREVIOUS_BALL_WEIGHT #PREVIOUS_BALL_WEIGHT - (PREVIOUS_BALL_WEIGHT / ball_max_dist / 2) * ball_dist

        prediction_score = 0
        if self.prediction is not None and self.ball is not None:
            ball_dist = (point.sub(self.ball)).length()
            prediction_dist = (point.sub(self.prediction)).length()
            # prediction_score = PREDICTION_WEIGHT * math.pow(math.e, -2 * prediction_dist)
            prediction_score += PREDICTION_WEIGHT - (PREDICTION_WEIGHT / 1) * ball_dist

        return detection_score + previous_ball_score + prediction_score

    def get_basepoints(self):
        return self.basepoints_data

    def get_particles(self):
        return [p[0] for p in self.particles]
