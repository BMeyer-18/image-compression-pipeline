from ProcessImage import compress_image

# COMPRESS
in_path = "./data/gradient.jpg"
out_path = "./data/grad_compressed.bin"
k = 3
compress_image(in_path, out_path, k)

# DECOMPRESS
# load compressed bin file
# separate out image data and metadata/codes
# decompress with reverse lempel ziv
# replace huffman codes with colors
# write to image