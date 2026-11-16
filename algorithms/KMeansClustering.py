from algorithms.KDSearch import buildKDTree, searchKDTree
from algorithms.Helpers import calculateSqDistance
from random import randrange, random

def cluster(data, k):
    """
    cluster
    """
    centroids = pickCentroids(data, k)

    while True:
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


def pickCentroids(data, k):
    """
    kmeans++
    """
    # choose random point to be first centroid
    centroids = [data[randrange(len(data))]]

    # choose other k-1 centroids (points likely far from already-selected centroids)
    while len(centroids) < k:
        # make k-d tree of centroids
        tree = buildKDTree(centroids)

        # find all points' distance to closest centroid using k-d search
        sqDists = []
        for point in data:
            closest = searchKDTree(tree, point)
            sqDists.append(calculateSqDistance(closest, point))
        total = sum(sqDists)
        threshold = random()*total
        cumulativeSum = 0.0
        for idx in range(len(data)):
            cumulativeSum += sqDists[idx]
            if cumulativeSum >= threshold:
                centroids.append(data[idx])
                break
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