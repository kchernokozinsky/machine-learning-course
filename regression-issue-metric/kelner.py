import math


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
        return 2.71828182846 ** (-2 * r ** 2)
    else:
        return 0