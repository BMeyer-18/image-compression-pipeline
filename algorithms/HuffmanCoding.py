def build_huffman_tree(freqs):
    """
    build tree based on frequencies of each color
    """
    tree = list(freqs.keys())
    while len(tree) > 1:
        tree.sort(key=lambda val: freqs[val])
        right = tree.pop(0)
        left = tree.pop(0)
        branch = (left, right)
        freqs[branch] = freqs[left] + freqs[right]
        del freqs[left], freqs[right]
        tree.append(branch)
    return tree[0]

def get_huffman_codes(tree):
    """
    get dict of colors and codes
    """
    codes = {}
    for i in range(len(tree)):
        if len(tree[i]) == 3:
            # if the tuple is a color, record its code
            codes[tree[i]] = f"{i}"
        else:
            # if the tuple is a subtree, search deeper and add 1s/0s
            subcodes = get_huffman_codes(tree[i])
            for key in subcodes.keys():
                subcodes[key] = f"{i}{subcodes[key]}"
            codes |= subcodes
    return codes