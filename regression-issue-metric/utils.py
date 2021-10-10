# fixed
import random

mistaken_data = dict()


def function(x):
    return 1 / (1 + 25 * x ** 2)


def reset_mistaken_data():
    global mistaken_data
    mistaken_data = dict()


def function_with_mistakes(x):
    global mistaken_data
    if x in mistaken_data.keys():
        return mistaken_data[x]
    y = 1 / (1 + 25 * x ** 2)
    if random.randint(0, 50) == 1:
        y *= 10
    mistaken_data[x] = y
    return y


def get_training_data(l):
    data = []
    for i in range(1, l + 1):
        x = 4 * (i - 1) / (l - 1) - 2
        data.append(x)
    return data


def get_testing_data(l):
    data = []
    for i in range(1, l):
        x = 4 * (i - 0.5) / (l - 1) - 2
        data.append(x)
    return data


def r_fixed(u, x, h: float):
    return abs(u - x) / h


def r_changing(u, x1, x2):
    return float(abs(u - x1) / abs(u - x2))
