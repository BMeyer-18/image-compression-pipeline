def encode_colors(image):
    """
    get code for each color
    """
    dims = image.size
    pixels = list(image.getdata())


def map_freqs(colors):
    """
    get frequency of each color
    """
    freqs = {color: 0 for color in set(colors)}
    for color in colors:
        freqs[color] += 1
    return freqs