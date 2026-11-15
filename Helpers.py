from math import sqrt

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


def calculateDistance(point1, point2):
    """
    euclidean distance
    """
    return sqrt(calculateSqDistance(point1, point2))