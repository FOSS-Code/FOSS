import time

import numpy as np
import math
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from queue import Queue

from distance_utils import path_distance


def class_clustering(data, k=3):
    # data:np
    # sample number
    m, n = data.shape
    c_pos = np.random.randint(0, m, size=k)
    list = np.zeros((m,))
    cluster = {}
    center = {}
    # data center
    for c in range(k):
        cluster[c] = []
        center[c] = data[c_pos[c]]
    while True:
        # iterate
        for p in range(m):
            dist_max = 10000000
            res = -1
            for c in range(k):
                dist_temp = np.sum((data[p] - center[c]) ** 2)
                if dist_temp < dist_max:
                    dist_max = dist_temp
                    res = c
            list[p] = res
        canBreak = True
        # update
        for c in range(k):
            c_temp = np.mean(data[list == c], axis=0)
            if not all(c_temp == center[c]):
                canBreak = False
                center[c] = c_temp
        if canBreak:
            break
    return list


def basa(data, threshold, max_k):
    # data:np
    m, n = data.shape[0]
    center = {}
    cluster = {}
    center[0] = data[0, :]
    cluster[0] = []
    cluster[0].append(0)
    for p in range(1, m):
        dist_min = 10000000
        res = -1
        for c in len(center):
            dist_temp = np.sqrt(np.sum(center[c] - data[p]) ** 2)
            if dist_temp < dist_min:
                dist_min = dist_temp
                res = c
        if dist_min > threshold and len(cluster) < max_k:
            cur = len(cluster)
            cluster[cur] = []
            cluster[cur].append(p)
            center[cur] = data[p]
        else:
            center[res] = (center[res] * len(cluster[res]) + data[p]) / (len(cluster[res] + 1))
            cluster[res].append(p)

    return cluster


def hierarchical(data, min_k=1):
    # data:np
    m, n = data.shape
    dist = np.zeros((m, m))
    cluster = {}
    for i in range(m):
        cluster[i] = []
        cluster[i].append(i)
    for i in range(m):
        for j in range(i + 1, m):
            dist[i, j] = np.sqrt(np.sum((data[i] - data[j]) ** 2))
            dist[j, i] = dist[i, j]
    print(dist)
    cur_k = m
    while cur_k > min_k:
        dist_min = 1000000
        res = []
        for i in range(cur_k):
            for j in range(i + 1, cur_k):
                if dist[i, j] < dist_min:
                    dist_min = dist[i, j]
                    res = [i, j]
        for i in range(cur_k):
            dist[res[0], i] = np.minimum(dist[res[0], i], dist[i, res[1]])
            dist[i, res[0]] = dist[res[0], i]
        dist = np.delete(dist, res[1], axis=0)
        dist = np.delete(dist, res[1], axis=1)
        cluster[res[0]] = cluster[res[0]] + cluster[res[1]]
        for i in range(res[1], cur_k - 1):
            cluster[i] = cluster[i + 1]

        cluster.pop(cur_k - 1)
        cur_k -= 1

    return cluster


def dbscan(data, e, minpts):
    omega = []
    Ne = {}
    C = {}
    m, n = len(data), len(data[0])
    for i in range(m):
        start = time.time()
        Ne[i] = []
        for j in range(m):
            # print(path_distance(data[i], data[j]))
            if path_distance(data[i], data[j]) <= e ** 2:
                Ne[i].append(j)
        print('[DONE] [{0}/{1}] {2:.2f} s'.format(i, m, time.time() - start))
        if len(Ne[i]) >= minpts:
            omega.append(i)
    k = 0
    vis = np.zeros((m,))
    while len(omega) > 0:
        ck = []
        q = Queue()
        if len(omega) > 1:
            o = omega[np.random.randint(0, len(omega) - 1)]
        else:
            o = omega[0]
        q.put(o)
        vis[o] = 1
        ck.append(o)

        while not q.empty():
            head = q.get()
            if len(Ne[head]) >= minpts:
                for ht in Ne[head]:
                    if vis[ht] == 0:
                        vis[ht] = 1
                        q.put(ht)
                        ck.append(ht)

        for c in ck:
            if c in omega:
                omega.remove(c)
        C[k] = ck
        k = k + 1
    return C


def mixGaussian(data, k, epochs):
    m, n = data.shape
    alpha = np.ones((k,)) / k
    mu = np.zeros((k, n))
    pos_init = np.random.randint(0, m, size=k)
    for i in range(k):
        mu[i] = data[pos_init[i]]
    sigma = np.zeros((k, n, n))
    for i in range(k):
        sigma[i] = np.eye(n) * 0.1
    gamma = np.zeros((m, k))

    for epoch in range(epochs):
        for j in range(m):
            sum = 0
            for i in range(k):
                gamma[j][i] = alpha[i] * np.exp((np.dot(
                    np.dot(data[j:j + 1, :] - mu[i:i + 1, :], np.linalg.inv(sigma[i])),
                    (data[j:j + 1, :] - mu[i:i + 1, :]).T)) / (-2)) / (
                                          np.power(2 * math.pi, n / 2) * np.sqrt(np.abs(np.linalg.det(sigma[i]))))
                sum += gamma[j][i]
            gamma[j:j + 1, :] /= sum
        for i in range(k):
            mt = np.zeros((1, n))
            st = np.zeros((n, n))
            for j in range(m):
                mt += gamma[j][i] * data[j:j + 1, :]
            mt /= np.sum(gamma[:, i:i + 1])
            mu[i:i + 1, :] = mt
            for j in range(m):
                st += gamma[j][i] * np.dot((data[j:j + 1, :] - mu[i:i + 1, :]).T, (data[j:j + 1, :] - mu[i:i + 1, :]))
            st /= np.sum(gamma[:, i:i + 1])
            sigma[i] = st
            alpha[i] = np.sum(gamma[:, i:i + 1]) / m
    cluster = {}
    for i in range(k):
        cluster[i] = []
    for j in range(m):
        sum = 0
        for i in range(k):
            gamma[j][i] = alpha[i] * np.exp((np.dot(np.dot(data[j:j + 1, :] - mu[i:i + 1, :], np.linalg.inv(sigma[i])),
                                                    (data[j:j + 1, :] - mu[i:i + 1, :]).T)) / (-2)) / (
                                      np.power(2 * math.pi, n / 2) * np.sqrt(np.abs(np.linalg.det(sigma[i]))))
            sum += gamma[j][i]
        gamma[j:j + 1, :] /= sum
    for j in range(m):
        res = np.argmax(gamma[j])
        cluster[res].append(j)
    return cluster