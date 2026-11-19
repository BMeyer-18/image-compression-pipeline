from algorithms.KDSearch import buildKDTree, searchKDTree
import numpy as np
from random import randrange, random

def cluster(data, k, max_iter=300):
    """
    cluster
    """
    centroids = pickCentroids(data, k)
    print('picked centroids')
    iterations = 0

    while iterations < max_iter:
        iterations += 1

        # sort points into clusters based on current centroids
        dists = np.zeros((len(data), len(centroids)))
        for i in range(len(centroids)):
            # set a column of dists to each point's distance from the centroid at that index
            dists[:,i] = np.linalg.norm(data - centroids[i], axis=1)
        # get a vector of the same size as data, in which each value is the index of the closest centroid
        labels = dists.argmax(axis=1)

        # recalculate centroids based on clusters
        newCentroids = np.array([calculateCentroid(data, labels, c) for c in range(len(centroids))])

        # check convergence
        if areCentroidsEqual(centroids, newCentroids):
            return centroids, labels
        
        centroids = newCentroids
        print(f"completed iteration {iterations}")
    return centroids, labels


def pickCentroids(data, k):
    """
    kmeans++
    """
    # choose random point to be first centroid
    centroids = np.array([data[randrange(len(data))]])

    # choose other k-1 centroids (points likely far from already-selected centroids)
    while len(centroids) < k:
        # find all points' distance to closest centroid using NumPy matrix operations
        dists = np.zeros((len(data), len(centroids)))
        for i in range(len(centroids)):
            # set a column of dists to each point's distance from the centroid at that index
            dists[:,i] = np.linalg.norm(data - centroids[i], axis=1)
        
        # condense dists to a vector with only the smallest distance to a centroid
        sqDists = dists.min(axis=1) ** 2

        # set threshold based on sum, and find first point where data passes index
        threshold = random() * sqDists.sum()
        centroids = np.append(centroids, [data[np.where(sqDists.cumsum() >= threshold)[0][0]]], axis=0)
        print(f"picked centroid {len(centroids)}")
    return centroids


def calculateCentroid(data, labels, c):
    """
    MAKE CENTROID OR DEFAULT
    """
    idc = labels == c
    if sum(idc) == 0:
        return data[randrange(len(data))]
    return data[idc].mean(axis=0)


def areCentroidsEqual(centroids1, centroids2):
    """
    check centroid equality
    """
    # make sure they have equal numbers of elements
    if len(centroids1) != len(centroids2):
        return False

    # sort arrays to get the same order, then check equality
    return np.array_equal(np.sort(centroids1, axis=0), np.sort(centroids2, axis=0))