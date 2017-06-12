from Point import Point


class Particle:
    def __init__(self, position, velocity, acceleration):
        self.position_ = position
        self.velocity_ = velocity
        self.acceleration_ = acceleration

    def getPosition(self):
        return self.position_

    def updateVelocity(self, timeDelta):
        self.velocity_.x = self.velocity_.x + timeDelta * self.acceleration_.x
        self.velocity_.y = self.velocity_.y + timeDelta * self.acceleration_.y

    def updatePosition(self, timeDelta):
        self.position_.x = self.position_.x + timeDelta * self.velocity_.x
        self.position_.y = self.position_.y + timeDelta * self.velocity_.y
