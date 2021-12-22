from itertools import product
import numpy as np
from tqdm import trange

PRACTICE = False
PADDING = 200
TRIM_AT_END = 50
NUM_ITERS = 50

with open("test.txt" if PRACTICE else "input.txt", "r") as f:
    content = f.read().strip()

enhancement_alg_str, image_str = content.split("\n\n")
enhancement_alg = [c == "#" for c in enhancement_alg_str]

def enhance(image_padded):
    image_conv = np.lib.stride_tricks.sliding_window_view(image_padded, (3, 3))
    height, width = image_padded.shape
    image_conv_reshaped = image_conv.reshape((height - 2, width - 2, 9))

    res = np.empty((height - 1, width - 1), dtype=bool)
    for i in range(height - 2):
        for j in range(width - 2):
            alg_idx = list(image_conv_reshaped[i, j, :])
            binary_num = "".join(str(int(x)) for x in alg_idx)
            res[i, j] = enhancement_alg[eval(f"0b{binary_num}")]
    return res

image = np.array([
    [c == "#" for c in line]
    for line in image_str.split("\n")
], dtype=bool)
height, width = image.shape
image_padded = np.zeros((height + 2 * PADDING, width + 2 * PADDING), dtype=bool)
image_padded[PADDING:-PADDING,PADDING:-PADDING] = image[:, :]

curr = np.copy(image_padded)
for _ in trange(NUM_ITERS):
    curr = enhance(curr)

print(np.count_nonzero(curr[TRIM_AT_END:-TRIM_AT_END, TRIM_AT_END:-TRIM_AT_END]))
