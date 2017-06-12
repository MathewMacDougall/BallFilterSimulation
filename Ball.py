from Point import Point


class Ball:
    def __init__(self, x, y, vx=0, vy=0, lock_time=0):
        self.pos = Point(x, y)
        self.vel = Point(vx, vy)
        self.lock_time = lock_time # the last timestamp the ball was seen/updated

    def position(self):
        return self.pos

    def velocity(self):
        return self.vel

    def lock_time(self):
        return self.lock_time

    def update_position(self, new_pos, timestamp):
        last_pos = self.pos
        self.pos = new_pos
        last_timestamp = self.lock_time
        self.lock_time = timestamp

        dt = self.lock_time - last_timestamp
        dist = (self.pos.sub(last_pos)).length()
        self.vel = (self.pos.sub(last_pos)).norm(dist / dt)

    def copy(self):
        return Ball(self.pos.x, self.pos.y, self.vel.x, self.vel.y, self.lock_time)

    def __str__(self):
        return "x: {}, y:{}, vx: {}, vy: {}, ts: {}".format(self.pos.x, self.pos.y, self.vel.x, self.vel.y,
                                                            self.lock_time)

    def __repr__(self):
        return "x: {}, y:{}, vx: {}, vy: {}".format(self.pos.x, self.pos.y, self.vel.x, self.vel.y,
                                                    self.lock_time)
