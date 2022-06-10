import random
import numpy as np
import collections
import joblib


def cal_single_entropy(p):
    return p*np.log2(1.0/p)


def cal_entropy(p_list):
    sum = 0
    for p in p_list:
        sum += cal_single_entropy(p)
    return sum


def monte_carlo_attr(id, data, params, cal_sum=False, iter=5, save=True):
    """
    :param id: node id
    :param data: data[indexSub, :]
    :param params: params
    :param cal_sum
    :param iter
    :param save
    :return
    """

    min_d = None
    min_h = None
    tmp_data = {'node_id': id, 'data': data, 'cal_sum': cal_sum, 'iter': iter, 'tmp_data': []}

    for i in range(iter):
        # random dim
        candidate_d = random.randint(0, params['numDim'] - 1)

        # normalize data
        max_num_in_d = np.max(data[:, candidate_d])
        min_num_in_d = np.min(data[:, candidate_d])
        data[:, candidate_d] = (data[:, candidate_d] - min_num_in_d) / (max_num_in_d - min_num_in_d)

        # calc probability
        p_dict = collections.Counter(data[:, candidate_d])
        for key in p_dict:
            p_dict[key] /= data.shape[0]

        # calc hx
        h = 0
        mean_num_in_d = np.mean(data[:, candidate_d])
        if not cal_sum:
            for key in p_dict:
                h += cal_single_entropy(p_dict[key]) / abs(key - mean_num_in_d)
        else:
            h = cal_entropy(p_dict.values()) / np.sum(abs(data[:, candidate_d] - mean_num_in_d))

        # update
        if i == 0:
            min_d = candidate_d
            min_h = h
        else:
            if min_h > h:
                min_h = h
                min_d = candidate_d

        # save data
        tmp_data['tmp_data'].append({
            'iter': i,
            'candidate_d': candidate_d,
            'p_dict': p_dict,
            'data_of_d': data[:, candidate_d],
            'mean_num_in_d': mean_num_in_d,
            'h': h,
        })

    if save:
        joblib.dump(tmp_data, './monte_carlo_tmp_data/node_id_'+str(id)+'.joblib')

    return min_d
