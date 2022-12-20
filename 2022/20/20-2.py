import string
import re
import math
from collections import defaultdict
from enum import Enum
import itertools
import tqdm
from dataclasses import dataclass
import random

PRACTICE = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()
lines = file_content.split("\n")

labelled_numbers = [(i, 811589153 * int(l)) for i, l in enumerate(lines)]
file_size = len(labelled_numbers)

for _ in range(10):
    for id_to_move in range(file_size):
        old_idx = None
        for i, (k, n) in enumerate(labelled_numbers):
            if k == id_to_move:
                old_idx = i
                break
        assert old_idx is not None
        new_idx = (old_idx + n) % (file_size - 1)
        labelled_numbers.pop(old_idx)
        labelled_numbers.insert(new_idx, (k, n))

final_numbers = [n for _, n in labelled_numbers]
zero_idx = final_numbers.index(0)
print(sum(final_numbers[(zero_idx + x) % file_size] for x in (1000, 2000, 3000)))
