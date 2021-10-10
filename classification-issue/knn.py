import math
import operator
import random
from enum import Enum
from functools import cmp_to_key

import matplotlib.pyplot as plt

from Klass import Klass, is_inside
from Point import Point, get_distance

Q = 0.3


class WeightType(Enum):
    NONE = 1
    LINEAR = 2
    EXP = 3


def generate_klasses(x1_borders: list, x2_borders: list):
    klasses = list()
    x1_borders.sort()
    x2_borders.sort()
    for i in range(len(x1_borders) - 1):
        x1_1 = x1_borders[i]
        x1_2 = x1_borders[i + 1]
        for j in range(len(x2_borders) - 1):
            x2_1 = x2_borders[j]
            x2_2 = x2_borders[j + 1]
            klasses.append(Klass("class_" + str((i + 1) * (j + 1)), x1_1, x1_2, x2_1, x2_2))
    return klasses


def generate_all_points(number, x1_min, x1_max, x2_min, x2_max):
    points = list()
    for i in range(number):
        points.append(Point(random.uniform(x1_min, x1_max), random.uniform(x2_min, x2_max)))
    return points


def divide_points(points):
    learn_n = math.floor(len(points) / 3)
    return [points[: learn_n + 1], points[learn_n:]]


def set_learn_data(points: list, klasses: list):
    learn_data = dict()
    for p in points:
        for klass in klasses:
            if is_inside(p, klass):
                learn_data[p] = klass
                break
    return learn_data


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


def k_nearest_neighbours(point, learn_data: dict, k, mode):
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
        i +=1
    res_klass = max(stats.items(), key=operator.itemgetter(1))[0]

    return res_klass


def draw_points(points: list, size: int, color: str):
    for p in points:
        plt.scatter(p.x, p.y, s=size, color=color)


def draw(name, x1_borders: list, x2_borders: list, learn_data, data_to_learn, k, mode):
    plt.figure(name)
    x1_min = min(x1_borders)
    x1_max = max(x1_borders)
    x2_min = min(x2_borders)
    x2_max = max(x2_borders)
    plt.ylabel('x2')
    plt.xlabel('x1')
    plt.xlim([x1_min - 2, x1_max + 2])
    plt.ylim([x2_min - 2, x2_max + 2])
    # draw x1_boundaries
    for x1 in x1_borders:
        plt.plot([x1, x1], [x2_min, x2_max], color="black")

    # draw x2_boundaries
    for x2 in x2_borders:
        plt.plot([x1_min, x1_max], [x2, x2], color="black")

    draw_points(learn_data, 5, "blue")

    algorithm(k, mode, data_to_learn, learn_data)


def algorithm(k, mode, data_to_learn: list, learned_data: dict):
    hit = 0
    hitted = list()
    not_hitted = list()
    solved = dict()
    for p in data_to_learn:
        solved[p] = k_nearest_neighbours(p, learned_data, k, mode)
        if is_inside(p, solved[p]):
            hitted.append(p)
            hit += 1
        else:
            not_hitted.append(p)
    print("accuracy: %s/%s" % (hit, len(data_to_learn)))
    print("llo:", LLO(solved, k, mode))
    draw_points(hitted, 5, "green")
    draw_points(not_hitted, 5, "red")


def LLO(solved_data: dict, k, mode):
    llo = 0
    for p in solved_data.keys():
        new_learn_data = solved_data.copy()
        del new_learn_data[p]
        if solved_data[p] == k_nearest_neighbours(p, new_learn_data, k, mode):
            llo += 1
    return llo
