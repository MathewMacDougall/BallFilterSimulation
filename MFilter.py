from Point import Point
from BallData import BallData
from Ball import Ball
import math
from collections import deque
import Util

# import BallFilterSimulator

MAX_CLUSTER_VARIANCE = 0.05  # 5cm
MAX_BALL_SPEED = 8.5  # max is 8 with a bit of a buffer so we don't accidentally miss data
VISION_CONFIDENCE_THRESHOLD = 0.9
BALL_CONFIDENCE_THRESHOLD = 0
BALL_MAX_CONFIDENCE = 100
BALL_CONFIDENCE_INCREMENT = 20


class MFilter:
    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.data_ = []  # list of ball vision detections
        self.ball_ = None
        self.last_ball_ = self.ball_
        self.last_last_ball_ = self.last_ball_
        self.confidence = BALL_CONFIDENCE_THRESHOLD - 1

    def add(self, new_ball_data):
        self.data_.append(new_ball_data)

    # return the filtered ball
    def getEstimatedBall(self):
        if self.ball_ is None:
            return Point(0, 0) # This is a placeholder point
        else:
            return self.ball_

    # should compute new variance of vision data and set ball accordingly
    def update(self, timeDelta):
        # remove balls that either have low confidence or are out of the field
        datapoints = [] # a list of valid detected ball position
        for d in self.data_:
            if d.confidence > VISION_CONFIDENCE_THRESHOLD and Util.is_within_field(d.position(), self.length, self.width):
                datapoints.append(d.position())

        # shift history of balls
        self.last_last_ball_ = self.last_ball_
        self.last_ball_ = self.ball_

        ball_detected = len(datapoints) > 0  # did we get any detection data?
        current_ball_valid = self.last_ball_ is not None and self.confidence >= BALL_CONFIDENCE_THRESHOLD  # have we recently known the ball's location?
        has_noise = (Util.get_points_variance(datapoints) > MAX_CLUSTER_VARIANCE) if ball_detected else False  # are detected balls closely clustered or not?

        if not ball_detected:
            if current_ball_valid:
                print("no ball, valid")
                # There is no ball data this tick but we are confident enough in the last ball.
                # Return the last seen ball or predict where it would be
                # TODO: either return the ball's old position or predict where it would be based on it's velocity
                self.ball_ = self.ball_
                self.update_confidence(-BALL_CONFIDENCE_INCREMENT)
            else:
                print("no ball, not valid")
                # There is no ball data and we aren't confident in our last ball position
                # Don't do anything. Maybe return a placeholder?
                # self.confidence = BALL_CONFIDENCE_THRESHOLD - 1
                return
        else:  # ball detected
            if current_ball_valid:

                # TODO: Filter the noise, maybe finding a line with old balls
                point = self.ball_
                if has_noise:
                    print("ball and valid with noise")
                    for p in datapoints:
                        linear = Util.points_are_linear([self.last_last_ball_, self.last_ball_, p], 5 * math.pi / 180)
                        # print("linear: {}".format(linear))
                        if linear:
                            point = p
                            break
                        else:
                            point = Util.get_closest(self.last_ball_, datapoints)
                else:
                    print("ball and valid, no noise")
                    # point = Util.average_points(datapoints)
                    point = datapoints[len(datapoints) - 1]

                if Util.is_valid_velocity(self.last_ball_, point, timeDelta, MAX_BALL_SPEED):
                    self.ball_ = point
                    self.update_confidence(BALL_CONFIDENCE_INCREMENT)
                else:
                    self.ball_ = self.ball_
                    self.update_confidence(-BALL_CONFIDENCE_INCREMENT)
            else:
                print("ball and not valid")
                # Just use vision data. It's our best bet since we don't know where the ball was previously
                # TODO: either take the newest detection or average them. could use centroid function again
                self.ball_ = datapoints[len(datapoints) - 1]
                # self.update_confidence(BALL_CONFIDENCE_INCREMENT)
                self.confidence = BALL_MAX_CONFIDENCE / 2

        self.data_.clear() # remove data for next tick


    # increments the confidence by val without going out of range
    def update_confidence(self, val):
        newval = self.confidence + val
        if newval > BALL_MAX_CONFIDENCE:
            self.confidence = BALL_MAX_CONFIDENCE
        if newval < BALL_CONFIDENCE_THRESHOLD:
            self.confidence = BALL_CONFIDENCE_THRESHOLD - 1
