from math import sqrt
from random import randrange, random

def cluster(data, k):
    """
    cluster
    """
    clusters = [[] for i in range(k)]


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
    


def calculateSqDistance(point1, point2):
    """
    squared euclidean distance
    """
    if len(point1) != len(point2):
        raise ValueError("Points do not have same numbers of coordinates")
    sum = 0
    for i in range(len(point1)):
        sum += (point2[i] - point1[i])**2
    return sum