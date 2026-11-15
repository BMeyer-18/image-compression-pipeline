from KMeansClustering import cluster
from KDSearch import *

data = [[0, 1], [2, 3], [0, 2], [5, 6], [5, 1]]
#clusters = cluster(data, 2)
#print(clusters)


tree = buildKDTree(data)
closest = searchKDTree(tree, [0, 10])
print(closest)