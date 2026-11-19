from PIL import Image
from sklearn.cluster import KMeans
import numpy as np
from algorithms.KDSearch import buildKDTree, searchKDTree
from algorithms.KMeansClustering import cluster
from algorithms.HuffmanCoding import build_huffman_tree, get_huffman_codes
from algorithms.LempelZiv import encode_lz

def compress_image(input_path, output_path, k):
    """
    driver function for image compression
    """
    # load image
    image = Image.open(input_path).convert('RGB')
    dims = image.size
    colors = np.array(image.getdata())

    # reduce colors in image (lossy)
    clusters, centroids = cluster(colors, k, max_iter=10)
    #kmeans = KMeans(n_clusters=8, random_state=0, n_init="auto").fit(colors)
    #centroids = kmeans.cluster_centers_
    #labels = kmeans.labels_
    rounded_centroids = np.array([tuple(round(c) for c in color) for color in centroids])
    print('completed clustering')
    reduced_colors = reduce_colors(colors, rounded_centroids)
    save_image(reduced_colors, dims, './data/dog_reduced.jpeg')
    print('reduced colors')

    # build Huffman tree and get codes
    freqs = {rounded_centroids[i]: len(clusters[i]) for i in range(len(clusters))}
    #freqs = {rounded_centroids[i]: sum(labels == i) for i in range(len(centroids))}
    print(freqs)
    tree = build_huffman_tree(freqs)
    codes = get_huffman_codes(tree)
    print('built huffman tree')

    # encode to binary string with Lempel-Ziv
    string, padding = encode_lz(reduced_colors, codes)
    metadata = generate_metadata_string(dims, padding, tree)
    print('finished encoding')

    # convert to bytes and write to file
    byte_data = convert_to_bytes(metadata + string)
    write_to_file(byte_data, output_path)
    print('finished compression')


def reduce_colors(colors, centroids):
    """
    replace every color with its centroid
    """
    tree = buildKDTree(centroids)
    reduced = []
    for color in colors:
        closest = searchKDTree(tree, color)
        reduced.append(closest)
    return reduced


def generate_metadata_string(dims, padding, tree):
    """
    Generate string of metadata to preface encoded image
    """
    tree_string = generate_tree_string(tree)
    comma = format(ord(','), '08b')
    return format(dims[0], '08b') + comma + format(dims[1], '08b') + comma + format(padding, '08b') + comma + tree_string


def generate_tree_string(tree):
    """
    generate string to represent tree
    """
    tree_string = ""
    for subtree in tree:
        if len(subtree) == 3:
            for color in subtree:
                tree_string += format(color, '08b')
        else:
            tree_string += format(ord('('), '08b') + generate_tree_string(subtree) + format(ord(')'), '08b')
    return tree_string


def convert_to_bytes(bit_string):
    """
    convert bits to bytes
    """
    byte_list = []
    for i in range(0, len(bit_string), 8):
        byte = bit_string[i:i+8]
        byte_list.append(int(byte, 2))

    return bytes(byte_list)


def write_to_file(byte_data, path):
    """
    write bytes to file
    """
    with open(path, 'wb') as f:
        f.write(byte_data)


def save_image(colors, dims, path):
    image = Image.new(mode="RGB", size=dims)
    image.putdata(colors)
    image.save(path, format="jpeg")