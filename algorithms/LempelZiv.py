from math import ceil, log2

def encodeLZ(string):
    """
    encode string with lempel ziv
    """
    # initialize variables
    codes = {}
    sequences = []
    chars = list(string)
    bit_string = ""

    # assign binary code of same length to each character
    # HUFFMAN CODING