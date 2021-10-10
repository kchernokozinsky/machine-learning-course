import matplotlib.pyplot as plt

from knn import generate_klasses, draw, WeightType, divide_points, generate_all_points, set_learn_data

X1_BORDERS = [-1, 2, 3]
X2_BORDERS = [2, -3, 3]
POINT_NUMBER = 400
POINTS = []

if __name__ == '__main__':
    x1_min = min(X1_BORDERS)
    x1_max = max(X1_BORDERS)
    x2_min = min(X2_BORDERS)
    x2_max = max(X2_BORDERS)

    all_points = divide_points(generate_all_points(POINT_NUMBER, x1_min, x1_max, x2_min, x2_max))
    learn_data = set_learn_data(all_points[0], generate_klasses(X1_BORDERS, X2_BORDERS))
    data_to_learn = all_points[1]

    for k in range(1, 3):
        print("------------------------------")
        print("K = %s, WeightType = Linear" % k)
        draw("K = %s, WeightType = Linear" % k, X1_BORDERS, X2_BORDERS, learn_data, data_to_learn, k, WeightType.LINEAR)
    #
    # for k in range(1, 5):
    #     print("------------------------------")
    #     print("K = %s, WeightType = None" % k)
    #     draw("K = %s, WeightType = None" % k, X1_BORDERS, X2_BORDERS, learn_data, data_to_learn, k, WeightType.NONE)
    #
    # for k in range(1, 5):
    #     print("------------------------------")
    #     print("K = %s, WeightType = Exp" % k)
    #     draw("K = %s, WeightType = Exp" % k, X1_BORDERS, X2_BORDERS, learn_data, data_to_learn, k, WeightType.EXP)

    plt.show()
