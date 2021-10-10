import math

from Point import get_distance


def get_points_by_class(points_dict, klass):
    points = list()
    for p in points_dict.keys():
        if points_dict[p] == klass:
            points.append(p)
    return points


def standard_method(percentage, points_dict, klasses):
    p_d = dict()
    for klass in klasses:
        points = get_points_by_class(points_dict, klass)
        new_num = len(points) / 100 * percentage
        for i in range(int(new_num)):
            standard = calculate_standard(points)
            p_d[standard] = klass
            points.remove(standard)
    return p_d


def calculate_standard(points: list):
    min_p = math.inf
    standard = None
    for p in points:
        sum = 0
        for p1 in points:
            sum += get_distance(p, p1)
        if sum < min_p:
            standard = p
            min_p = sum
    return standard
