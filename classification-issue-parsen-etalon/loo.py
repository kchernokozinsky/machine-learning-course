from knn import k_nearest_neighbours
from parsen_window import learn_fixed, learn_chngd
from standard import standard_method


def loo(data_set: dict, h: float, k: int, percentage: float, klasses: list, is_knn: bool, kernel,
        mode, is_fixed):
    loo = 0
    if is_knn:
        for p in data_set.keys():
            new_learn_data = data_set.copy()
            del new_learn_data[p]
            if data_set[p] == k_nearest_neighbours(p, standard_method(percentage, new_learn_data, klasses), k, mode):
                loo += 1
        return loo
    else:
        if is_fixed:
            for p in data_set.keys():
                new_learn_data = data_set.copy()
                del new_learn_data[p]
                if data_set[p] == learn_fixed(p, h, standard_method(percentage, new_learn_data, klasses), kernel):
                    loo += 1
            return loo
        else:
            for p in data_set.keys():
                new_learn_data = data_set.copy()
                del new_learn_data[p]
                if data_set[p] == learn_chngd(p, standard_method(percentage, new_learn_data, klasses), kernel, k):
                    loo += 1
            return loo
