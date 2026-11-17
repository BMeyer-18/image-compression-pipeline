from PIL import Image
from algorithms.KMeansClustering import cluster
from algorithms.HuffmanCoding import build_huffman_tree, get_huffman_codes
from algorithms.LempelZiv import encodeLZ
from ProcessImage import *

# COMPRESS
# load image
path = "./data/gradient.jpg"
image = Image.open(path).convert('RGB')
dims = image.size
colors = list(image.getdata())

# reduce colors in image (lossy)
clusters, centroids = cluster(colors, 3)
rounded_centroids = [tuple(round(c) for c in color) for color in centroids]
reduced_colors = reduce_colors(colors, rounded_centroids)
#save_image(reduced_colors, dims, './data/gradient_reduced.jpeg')

# compress to binary
freqs = {rounded_centroids[i]: len(clusters[i]) for i in range(len(clusters))}
print(freqs)
tree = build_huffman_tree(freqs)
codes = get_huffman_codes(tree)
print(tree)
print(codes)

#codes = encode_colors(image)
# compress with lempel ziv
# save to file


# DECOMPRESS
# load compressed bin file
# separate out image data and metadata/codes
# decompress with reverse lempel ziv
# replace huffman codes with colors
# write to image