import numpy as np


def path_distance_one_dim(path_a, path_b):
    len_a = len(path_a)
    len_b = len(path_b)
    common_prefix = 0
    for i in range(min(len_a, len_b)):
        if path_a[i] == path_b[i]:
            common_prefix += 1
        else:
            break
    return np.exp(-2 * common_prefix / (len_a + len_b))


def path_distance(paths_a, paths_b):
    len_a = len(paths_a)
    len_b = len(paths_b)
    if len_a != len_b:
        raise ValueError('Path_A and Path_B should have same dimension')
    dis = 0
    for i in range(len_a):
        dis += path_distance_one_dim(paths_a[i], paths_b[i])
    return dis
