from QuickSelect import quickselect
from Helpers import calculateDistance
from random import random

class Node:
    """
    store node info
    """
    def __init__(self, median=None, left=None, right=None, value=None):
        """
        initialize properties
        """
        self.median = median
        self.left = left
        self.right = right
        self.value = value


def buildKDTree(data, dim=0):
    """
    make tree for searching
    """
    # base cases
    if len(data) == 0:
        return Node()
    if len(data) == 1:
        return Node(value=data[0])

    # find median along specified dimesion; create root node
    median = quickselect(data, dim)
    root = Node(median=median)

    # continue iterating through dims, or reset to 0
    nextDim = 0
    if dim < len(data[0])-1:
        nextDim = dim + 1

    # check for small sets that could get stuck infinitely on a median
    vals = set([point[dim] for point in data])
    if len(vals) == 1:
        leftData = data[:len(data)//2]
        leftTree = buildKDTree(leftData, nextDim)
        rightData = data[len(data)//2:]
        rightTree = buildKDTree(rightData, nextDim)
        return Node(median=data[0][dim], left=leftTree, right=rightTree)
    if len(vals) == 2:
        leftData = [point for point in data if point[dim] == min(vals)]
        leftTree = buildKDTree(leftData, nextDim)
        rightData = [point for point in data if point[dim] == max(vals)]
        rightTree = buildKDTree(rightData, nextDim)
        return Node(median=max(vals), left=leftTree, right=rightTree)

    # add to left subtree
    leftData = [point for point in data if point[dim] < median]
    root.left = buildKDTree(leftData, nextDim)

    # add to right subtree
    rightData = [point for point in data if point[dim] >= median]
    root.right = buildKDTree(rightData, nextDim)

    # return tree (or subtree)
    return root


def searchKDTree(tree, query, dim=0):
    """
    search through tree
    """
    # if the node is a leaf, return its value
    if tree.median == None:
        return tree.value

    # continue iterating through dims, or reset to 0
    nextDim = 0
    if dim < len(query)-1:
        nextDim = dim + 1

    # recurse through subtrees until reaching a leaf
    leaf = None
    if query[dim] < tree.median:
        leaf = searchKDTree(tree.left, query, nextDim)
    else:
        leaf = searchKDTree(tree.right, query, nextDim)

    # if query is closer to median than point, check alternate branch and return resulting leaf if closer
    if abs(query[dim] - tree.median) < calculateDistance(query, leaf):
        altLeaf = None
        if query[dim] < tree.median:
            altLeaf = searchKDTree(tree.right, query, nextDim)
        else:
            altLeaf = searchKDTree(tree.left, query, nextDim)

        if calculateDistance(query, leaf) <= calculateDistance(query, altLeaf):
            return leaf
        else:
            return altLeaf

    # if located leaf is closer than median, return it
    return leaf
