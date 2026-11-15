from random import random, randrange

class Node:
    def __init__(self, median=None, left=None, right=None, value=None):
        self.median = median
        self.left = left
        self.right = right
        self.value = value


def buildKDTree(data, dim=0):
    # basw cases
    if len(data) == 0:
        return Node()
    if len(data) == 1:
        return Node(value=data[0])

    

    return 1
