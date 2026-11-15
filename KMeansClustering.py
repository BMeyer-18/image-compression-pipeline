from math import sqrt
from random import randrange, random
from Helpers import calculateSqDistance

def cluster(data, k):
    """
    cluster
    """
    centroids = pickCentroids(data, k)

    while True:
        # make empty cluster
        clusters = [[] for i in range(k)]

        # fill clusters based on current centroids
        for i in range(len(data)):
            closestIdx = 0
            minDistance = calculateSqDistance(data[i], centroids[0])
            # add point to cluster with nearest centroid
            # REPLACE WITH K-D TREE SEARCH?
            for j in range(1,len(centroids)):
                dist = calculateSqDistance(data[i], centroids[j])
                if dist < minDistance:
                    minDistance = dist
                    closestIdx = j
            clusters[closestIdx].append(data[i])

        # recalculate centroids based on clusters
        newCentroids = [calculateCentroid(cluster, data) for cluster in clusters]

        # check convergence
        if areCentroidsEqual(centroids, newCentroids):
            return clusters
        centroids = newCentroids


def pickCentroids(data, k):
    """
    kmeans++
    """
    # choose random point to be first centroid
    centroids = [data[randrange(len(data))]]

    # choose other k-1 centroids (points likely far from already-selected centroids)
    while len(centroids) < k:
        # find all points' distance to closest centroid
        #REPLACE W/ K-D TREE???
        sqDists = []
        for point in data:
            minDist = calculateSqDistance(point, centroids[0])
            for idx in range(1,len(centroids)):
                dist = calculateSqDistance(point, centroids[idx])
                if dist < minDist:
                    minDist = dist
            sqDists.append(minDist)
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
    return centroid


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