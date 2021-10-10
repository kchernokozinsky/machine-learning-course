import math
import random

from Klass import Klass, is_inside
from Point import Point


def accuracy(solved: dict, klasses):
    hit = 0
    for p in solved.keys():
        if is_inside(p, solved[p]):
            hit += 1
    return hit


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
