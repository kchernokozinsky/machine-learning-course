from enum import Enum
from functools import cmp_to_key

from utils import *


class Mode(Enum):
    FIXED = 1
    CHANGING = 2


class NadarayaWatsonModel:
    def __init__(self, data, origin_function, h, kernel, mode, k = 0):
        self.__origin_function = origin_function
        self.__data = sorted(data)
        self.__kernel = kernel
        self.__mode = mode
        self.__h = h
        self.__k = k

    def calculate(self, x):
        top_sum = 0
        down_sum = 0
        xs = self.get_appropriate_xs(x)
        if self.__mode == Mode.FIXED:
            for xi in xs:
                r = r_fixed(x, xi, self.__h)
                k_val = self.__kernel(r)
                top_sum += self.__origin_function(xi) * k_val
                down_sum += k_val
        elif self.__mode == Mode.CHANGING:
            data = sorted(self.__data, key=cmp_to_key(lambda z, y: compare(x, z, y)))
            data.reverse()
            for i in range(len(data) - 1):
                xi = data[i]
                xi2 = data[self.__k + 1]
                r = r_changing(x, xi, xi2)
                k_val = self.__kernel(r)
                top_sum += self.__origin_function(xi) * k_val
                down_sum += k_val
        return top_sum / down_sum

    def calculate_all(self, xs):
        ys = list()
        for x in xs:
            ys.append(self.calculate(x))
        return ys

    def get_appropriate_xs(self, x):
        xs = list()
        for xi in self.__data:
            if abs(x - xi) < self.__h:
                xs.append(xi)
        return xs

    def empirical_risk(self, data):
        loss = 0
        for i in range(len(data)):
            x = data[i]
            loss += (self.__origin_function(x) - self.calculate(x)) ** 2
        return loss


def compare(p, x, y):
    if abs(p - x) > abs(p - y):
        return -1
    elif abs(p - x) < abs(p - y):
        return 1
    else:
        return 0
