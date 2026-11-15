from KMeansClustering import cluster

data = [[0, 1], [2, 3], [0, 2], [5, 6], [5, 1]]
clusters = cluster(data, 2)
print(clusters)