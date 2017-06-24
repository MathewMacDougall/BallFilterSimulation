from Point import Point
import math

# returns true if the given point is within a field of length length (x dimension)
# and width width (y dimension) centered at (0, 0)
def is_within_field(point, length, width, tolerance=0):
    return math.fabs(point.x) < length / 2 + tolerance and math.fabs(point.y) < width / 2 + tolerance

# return the closest point to target
def get_closest(target, points):
    assert len(points) > 0

    min_dist = (points[0].sub(target)).length()
    closest = points[0]
    for p in points:
        dist = (p.sub(target)).length()
        if dist < min_dist:
            closest = p
            min_dist = dist

    return closest


# check if mathew_particle_ball is within 8m/s of old_ball
def is_valid_velocity(old_ball, new_ball, timeDelta, MAX_BALL_SPEED):
    dist = (new_ball.sub(old_ball)).length()
    vel = dist / timeDelta
    return vel < MAX_BALL_SPEED


# returns the variance of a list of poitns
def get_points_variance(cluster_data):
    assert len(cluster_data) > 0

    centroid = average_points(cluster_data)
    sum = 0

    for p in cluster_data:
        sum += ((p.sub(centroid)).length()) ** 2

    sum = sum / len(cluster_data)
    return math.sqrt(sum)


# takes a list of points
def average_points(datapoints):
    assert len(datapoints) > 0

    sum = Point(0, 0)
    for p in datapoints:
        sum = sum.add(p)

    sum = sum.norm(sum.length() / len(datapoints))
    return sum


# returns true if the datapoints are linear within tolerance and false otherwise
def points_are_linear(datapoints, tolerance):
    slopes = []
    if len(datapoints) < 3:
        return True
    else:
        angles = []
        for i in range(len(datapoints) - 1):
            if datapoints[i] is None or datapoints[i+1] is None:
                continue
            angles.append(datapoints[i].angle() - datapoints[i+1].angle())

        for a in range(len(angles) - 1):
            if math.fabs(angles[a] - angles[a+1]) > tolerance:
                return False

        return True

# return the variance of the given list of numbers
def get_variance(data):
    assert len(data) > 0

    sum = 0
    for d in data:
        sum += d

    average = sum / len(data)

    sum2 = 0
    for d in data:
        sum2 += d ** 2

    variance = sum2 / len(data) - average ** 2
    return variance
