from Point import Point


class Robot:
    def __init__(self, x=-99, y=-99, vx=0, vy=0):
        self.pos = Point(x, y)
        self.vel = Point(vx, vy)

    def position(self):
        return self.pos

    def velocity(self):
        return self.vel

    def copy(self):
        return Ball(self.pos.x, self.pos.y, self.vel.x, self.vel.y, self.timestamp)