# -*- coding: utf-8 -*-
"""KMeans.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_gBfQxRBlY5Qn3SsgtXBVg_72bgctHy6
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import pairwise_distances

def d(u, v):
    diff = u - v
    return diff.dot(diff)

def cost(X, R, M):
    cost = 0 
    for k in range(len(M)):
        diff = X - M[k]
        sq_distances = (diff * diff).sum(axis=1)
        cost += (R[:, k] * sq_distances).sum()
    return cost

def plot_k_means(X, K, max_iter=20, beta=3.0, show_plots=False):
    N, D = X.shape
    exponents = np.empty((N, K))

    #initialize M to random
    initial_centers = np.random.choice(N, K, replace=False)
    M = X[initial_centers]

    costs = []
    k = 0
    for i in range(max_iter):
        k += 1
        #step-1 determine assignments / responsibilities
        for k in range(K):
            for n in range(N):
                exponents[n,k] = np.exp(-beta*d(M[k], X[n]))
        R = exponents / exponents.sum(axis=1, keepdims=True)

        #step-2 recalculate means 
        M = R.T.dot(X) / R.sum(axis=0, keepdims=True).T

        c = cost(X, R, M)
        costs.append(c)

        if i > 0:
            if np.abs(costs[-1] - costs[-2]) < 1e-5:
                break

        if len(costs) > 1:
            if costs[-1] > costs[-2]:
                print("cost increased!")
                print("M:", M)
                print("R.min:", R.min(), "R.max:", R.max())

    if show_plots:
        plt.plot(costs)
        plt.title('Costs')
        plt.show()

        random_colors = np.random.random((K,3))
        colors = R.dot(random_colors)
        plt.scatter(X[:,0], X[:,1], c=colors) 
        plt.show()

    print("Final cost", costs[-1])
    return M, R


def get_simple_data():
    #assume 3 means 
    D = 2 #so we can visualize more easily
    s = 4 #separation so we can control how far apart the means are
    mu1 = np.array([0,0])
    mu2 = np.array([s,s])
    mu3 = np.array([0,s])

    N = 900 #number of samples
    X = np.zeros((N,D))
    X[:300, :] = np.random.randn(300,D) + mu1
    X[300:600, :] = np.random.randn(300, D) + mu2
    X[600:, :] = np.random.randn(300,D) + mu3
    return X

def main():
    X = get_simple_data()

    #what does it look like without clustering
    plt.scatter(X[:,0], X[:,1])
    plt.show()

    K=3
    plot_k_means(X, K, beta=1.0, show_plots=True)

    K = 3 
    plot_k_means(X, K, beta=3.0, show_plots=True)

    K = 3 
    plot_k_means(X, K, beta=10.0, show_plots=True)

    K = 5 #what happens if we choose a bad K
    plot_k_means(X, K, max_iter=30, show_plots=True)

    K = 5 #what happens when we change beta
    plot_k_means(X, K, max_iter=30, beta=0.3, show_plots=True)

if __name__ == '__main__':
    main()










