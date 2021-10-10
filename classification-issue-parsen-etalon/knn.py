import operator
from enum import Enum
from functools import cmp_to_key

from Point import get_distance

Q = 0.5


class WeightType(Enum):
    NONE = 1
    LINEAR = 2
    EXP = 3


def compare(p, x, y):
    if get_distance(p, x) > get_distance(p, y):
        return -1
    elif get_distance(p, x) < get_distance(p, y):
        return 1
    else:
        return 0


def w(i, k, w_type: WeightType):
    if w_type == WeightType.NONE:
        return 1
    elif w_type == WeightType.EXP:
        return Q ** i
    else:
        return (k + 1 - i) / k


def learn_all_knn(points, points_dict, k, mode):
    solved_data = dict()
    for p in points:
        solved_data[p] = k_nearest_neighbours(p, points_dict, k, mode)
    return solved_data


def k_nearest_neighbours(point, learn_data: dict, k:int, mode):
    sorted_points = sorted(learn_data.keys(), key=cmp_to_key(lambda x, y: compare(point, x, y)))
    sorted_points.reverse()
    sorted_points = sorted_points[:k]
    stats = dict()
    i = 1
    for p in sorted_points:
        klass = learn_data[p]
        if klass in stats:
            stats[klass] += 1.0 * w(i, k, mode)
        else:
            stats[klass] = 1.0 * w(i, k, mode)
        i += 1
    res_klass = max(stats.items(), key=operator.itemgetter(1))[0]

    return res_klass
