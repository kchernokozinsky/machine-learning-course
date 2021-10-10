import math
import random

X_MIN = 10
X_MAX = -10
Y_MIN = -10
Y_MAX = 10


def get_random_point(x_min, x_max, y_min, y_max):
    return random.uniform(x_min, x_max), random.uniform(y_min, y_max)


def k_means(objects: list, k):
    clusters = list()
    for _ in range(k):
        clusters.append(get_random_point(X_MIN, X_MAX, Y_MIN, Y_MAX))

    clusters_dict = distribute(clusters, objects)
    new_clusters = get_new_clusters(clusters_dict)
    while clusters != new_clusters:
        clusters = new_clusters
        clusters_dict = distribute(clusters, objects)
        new_clusters = get_new_clusters(clusters_dict)
    return clusters


def get_new_clusters(clusters_dict: dict):
    clusters = []
    for cl in clusters_dict.keys():
        x_avg = 0
        y_avg = 0
        for x, y in clusters_dict[cl]:
            x_avg += x
            y_avg += y
        x_avg /= len(clusters_dict[cl])
        y_avg /= len(clusters_dict[cl])
        clusters.append((x_avg, y_avg))
    return clusters


def distribute(clusters, objects):
    clusters_dict = dict()

    for cl in clusters:
        clusters_dict[cl] = []

    for x in objects:
        min_dist = math.inf
        fit_cluster = None
        for cl in clusters:
            dist = get_distance(x, cl)
            if dist < min_dist:
                min_dist = dist
                fit_cluster = cl
        clusters_dict[fit_cluster].append(x)

    return clusters_dict


def get_distance(p1: tuple, p2: tuple):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


if __name__ == '__main__':
    objects = []
    for i in range(300):
        objects.append(get_random_point(X_MIN, X_MAX, Y_MIN, Y_MAX))
    k = 3
    print(k_means(objects, k))