"""
A helper class to represent raw ball vision data
"""

from Point import Point


class BallData:
    def __init__(self, x, y, confidence):
        self.pos = Point(x, y)
        self.confidence = confidence

    def position(self):
        return self.pos

    def confidence(self):
        return self.confidence

    def __str__(self):
        return "x: {}, y:{}, confidence: {}".format(self.pos.x, self.pos.y, self.confidence)

    def __repr__(self):
        return "x: {}, y:{}, confidence: {}".format(self.pos.x, self.pos.y, self.confidence)
