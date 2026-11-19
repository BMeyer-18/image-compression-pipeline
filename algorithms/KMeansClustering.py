from algorithms.KDSearch import buildKDTree, searchKDTree
from algorithms.Helpers import calculateSqDistance
import numpy as np
from scipy import spatial
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

        # make empty cluster, k-d tree for centroids
        clusters = [[] for i in range(k)]
        tree = buildKDTree(centroids)

        # fill clusters based on current centroids
        for i in range(len(data)):
            # add point to cluster with nearest centroid using k-d search
            closest = searchKDTree(tree, data[i])
            closestIdx = centroids.index(closest)
            clusters[closestIdx].append(data[i])

        # recalculate centroids based on clusters
        newCentroids = [calculateCentroid(cluster, data) for cluster in clusters]

        # check convergence
        if areCentroidsEqual(centroids, newCentroids):
            return clusters, centroids
        centroids = newCentroids
        print(f"completed iteration {iterations}")
    return clusters, centroids


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


def calculateCentroid(cluster, data):
    """
    MAKE CENTROID OR DEFAULT
    """
    if len(cluster) == 0:
        return data[randrange(len(data))]
    centroid = [0 for _ in range(len(cluster[0]))]
    for i in range(len(cluster)):
        for j in range(len(cluster[0])):
            centroid[j] += cluster[i][j]
    for i in range(len(centroid)):
        centroid[i] /= len(cluster)
    return tuple(centroid)


def areCentroidsEqual(centroids1, centroids2):
    """
    check centroid equality
    """
    # make sure they have equal numbers of elements
    if len(centroids1) != len(centroids2):
        return False

    # check that every element in centroid 1 is in centroid 2 once
    for centroid in centroids1:
        if centroid not in centroids2:
            return False
        centroids2.remove(centroid)
    return True