from Point import Point
from Ball import Ball
from BallData import BallData
from Particle import Particle
import numpy as np
import math

PARTICLE_FILTER_DECAYRATE = 0.3
PARTICLE_FILTER_VAR_THRESH = 0.1  # unused


class ParticleFilter:
    def __init__(self, length, width):
        self.particles_ = []

        self.position_ = [Point(0, 0)] * 2
        self.positionVar_ = [Point(0, 0)] * 2

        self.velocity_ = [Point(0, 0)] * 2
        self.velocityVar_ = [Point(0, 0)] * 2

        self.acceleration_ = Point(0, 0)
        self.accelerationVar_ = Point(0, 0)

        self.estimateValid_ = False

        self.length_ = length
        self.width_ = width

        self.add(Point(0, 0))
        # set random seed

    def update(self, timeDelta):
        # update particle cloud parameters
        self.position_[1] = self.position_[0]
        self.positionVar_[1] = self.positionVar_[0]

        # TODO: maybe these should use the ball.velcity(time) functions or something other than 0
        self.position_[0] = Point(0, 0)
        self.positionVar_[0] = Point(0, 0)

        self.acceleration_.x = (self.velocity_[0].x - self.velocity_[1].x) / timeDelta
        self.acceleration_.y = (self.velocity_[0].y - self.velocity_[1].y) / timeDelta
        self.accelerationVar_.x = self.velocityVar_[0].x + self.velocityVar_[1].x
        self.accelerationVar_.y = self.velocityVar_[0].y + self.velocityVar_[1].y

        self.velocity_[1] = self.velocity_[0]
        self.velocityVar_[1] = self.velocity_[1]

        self.velocity_[0] = Point(0, 0)
        self.velocityVar_[0] = Point(0, 0)



        for i in sorted(range(len(self.particles_)), reverse=True):
            if np.random.randint(0, 100) >= PARTICLE_FILTER_DECAYRATE * 100:
                del self.particles_[i]  # delete the particle from the list
            else:
                self.particles_[i].updateVelocity(timeDelta)
                self.particles_[i].updatePosition(timeDelta)

    def add(self, ballLocation):
        if not math.isnan(ballLocation.x + ballLocation.y):
            self.particles_.append(Particle(ballLocation, self.velocity_[1], self.acceleration_))
            self.estimateValid_ = False

    def getEstimate(self):
        if self.estimateValid_ is False:
            self.updateEstimatedPartition()
            # print("Estimate not valid. updating")
        # else:
            # print("estimate valid")

        return self.position_[0]

    def getEstimateVariance(self):
        if self.estimateValid_ is False:
            self.updateEstimatedPartition()

        return self.positionVar_[0]

    def updateEstimatedPartition(self):
        sum = Point(0, 0)

        # Calculate mean of the points
        for p in self.particles_:
            sum.x += p.getPosition().x
            sum.y += p.getPosition().y

        self.position_[0].x = sum.x / len(self.particles_)
        self.position_[0].y = sum.y / len(self.particles_)

        sum = Point(0, 0)

        # Calculate the variance of the points
        for p in self.particles_:
            sum.x += (p.getPosition().x - self.position_[0].x) * (p.getPosition().x - self.position_[0].x)
            sum.x += (p.getPosition().y - self.position_[0].y) * (p.getPosition().y - self.position_[0].y)

        self.positionVar_[0].x = sum.x / len(self.particles_)
        self.positionVar_[0].y = sum.y / len(self.particles_)

        self.estimateValid_ = True
