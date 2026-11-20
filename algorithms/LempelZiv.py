from math import ceil, log2
import numpy as np
from algorithms.Helpers import pad_bit_string

def encode_lz(labels, codes):
    """
    encode labels with lempel ziv
    """
    # initialize variables
    labels_str = ''.join([str(label) for label in labels])
    sequences = np.array([])
    bit_string = ""

    # iterate through labels, adding new sequences where they appear to sequences and bit string
    current_sequence = ""
    for label in labels_str:
        current_sequence += label
        if np.where(sequences == current_sequence)[0].size == 0:
            reference = 0
            if len(current_sequence) > 1:
                reference = np.where(sequences == current_sequence[:-1])[0][0] + 1
            sequences = np.append(sequences, current_sequence)
            bit_string += pad_bit_string(format(reference, 'b'), ceil(log2(len(sequences))))
            bit_string += codes[int(label)]
            current_sequence = ""

    # add to bit string if a repeated combo is present in current_sequence
    if len(current_sequence) > 0:
        bit_string += pad_bit_string(format(np.where(sequences == current_sequence)[0][0] + 1, 'b'),
                                     ceil(log2(len(sequences) + 1)))

    padding = (8 - len(bit_string)%8)%8
    bit_string = padding*'0' + bit_string

    return bit_string, padding