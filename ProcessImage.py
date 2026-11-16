from algorithms.KDSearch import buildKDTree, searchKDTree
from PIL import Image

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


def save_image(colors, dims, path):
    image = Image.new(mode="RGB", size=dims)
    image.putdata(colors)
    image.save(path, format="jpeg")