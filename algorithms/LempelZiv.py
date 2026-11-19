from math import ceil, log2
import numpy as np
from algorithms.Helpers import pad_bit_string

def encode_lz(colors, codes):
    """
    encode string with lempel ziv
    """
    # initialize variables
    sequences = []
    bit_string = ""

    # iterate through colors, adding new sequences where they appear to table and bit string
    current_combo = []
    for color in colors:
        current_combo.append(color)
        if tuple(current_combo) not in sequences:
            reference = 0
            if len(current_combo) > 1:
                reference = sequences.index(tuple(current_combo[:-1]))+1
            sequences.append(tuple(current_combo))
            bit_string += pad_bit_string(format(reference, 'b'), ceil(log2(len(sequences))))
            bit_string += codes[color]
            current_combo = []

    # add to bit string if a repeated combo is present in current_combo
    if len(current_combo) > 0:
        bit_string += pad_bit_string(format(sequences.index(tuple(current_combo))+1, 'b'), ceil(log2(len(sequences) + 1)))

    padding = (8 - len(bit_string)%8)%8
    bit_string = padding*'0' + bit_string

    return bit_string, padding