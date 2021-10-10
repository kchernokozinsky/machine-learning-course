import math
import operator
from enum import Enum
from functools import cmp_to_key

from Point import get_distance, Point


class KernelType(Enum):
    P = 1
    T = 2
    E = 3
    Q = 4
    G = 5
    KNN = 6


def learn_all_parsen(points, h, points_dict, kernel, is_fixed, k):
    solved_data = dict()
    for p in points:
        if is_fixed:
            solved_data[p] = learn_fixed(p, h, points_dict, kernel)
        else:
            solved_data[p] = learn_chngd(p, points_dict, kernel, k)
    return solved_data


def learn_fixed(point: Point, h, points_dict: dict, kernel):
    # print(kernel)
    dataset = get_appropriate_points(point, points_dict, h)
    stats = dict()
    for p in dataset.keys():
        klass = dataset[p]
        r_val = r_fixed(point, p, h)
        if klass in stats:
            stats[klass] += kernel(r_val)
        else:
            stats[klass] = kernel(r_val)
    res_klass = max(stats.items(), key=operator.itemgetter(1))[0]

    return res_klass


def compare(p, x, y):
    if get_distance(p, x) > get_distance(p, y):
        return -1
    elif get_distance(p, x) < get_distance(p, y):
        return 1
    else:
        return 0


def learn_chngd(point: Point, points_dict: dict, kernel, k):
    stats = dict()
    dataset = sorted(points_dict.keys(), key=cmp_to_key(lambda x, y: compare(point, x, y)))
    for p in dataset:
        klass = points_dict[p]
        r_val = r_chngd(point, p, dataset[k+1])
        if klass in stats:
            stats[klass] += kernel(r_val)
        else:
            stats[klass] = kernel(r_val)
    res_klass = max(stats.items(), key=operator.itemgetter(1))[0]

    return res_klass


def get_appropriate_points(point, points_dict: dict, h):
    d_p = dict()
    for p in points_dict.keys():
        if get_distance(point, p) <= h:
            d_p[p] = points_dict[p]
    return d_p


# fixed
def r_fixed(u: Point, x: Point, h: float):
    return get_distance(u, x) / h


# changing
def r_chngd(u: Point, x1: Point, x2: Point):
    return get_distance(u, x1) / get_distance(u, x2)


def P(r: float):
    if -1 <= r <= 1:
        return 1
    else:
        return 0


def T(r: float):
    if -1 <= r <= 1:
        return 1 - abs(r)
    else:
        return 0


def E(r: float):
    if -1 <= r <= 1:
        return 1 - r ** 2
    else:
        return 0


def Q(r: float):
    if -1 <= r <= 1:
        return 1 - r ** 4
    else:
        return 0


def G(r: float):
    if -1 <= r <= 1:
        return math.exp(-2 * r ** 2)
    else:
        return 0
