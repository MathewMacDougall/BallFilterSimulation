import math


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def x(self):
        return self.x

    def y(self):
        return self.y

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def add(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def sub(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def norm(self, l=1):
        if self.length() < 0.00001:
            return Point(0, 0)
        else:
            return Point(self.x * l / self.length(), self.y * l / self.length())

    def angle(self):
        if self.length() == 0.0:
            return 0

        if self.y >= 0:
            return math.acos(self.x / self.length())
        else:
            return 2 * math.pi + math.acos(self.x / self.length())

    def copy(self):
        return Point(self.x, self.y)

    def __str__(self):
        return "<{}, {}>".format(self.x, self.y)

    def __repr__(self):
        return "<{}, {}>".format(self.x, self.y)

    @staticmethod
    def from_angle(angle, length):
        return Point(length * math.cos(angle), length * math.sin(angle))