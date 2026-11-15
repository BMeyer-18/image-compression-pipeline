from KMeansClustering import cluster
from KDSearch import *

data = [[0, 1], [2, 3], [0, 2], [5, 6], [5, 1]]
#clusters = cluster(data, 2)
#print(clusters)


median = quickselect(data, 0)
print(median)
print(data)