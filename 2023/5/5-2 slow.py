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
groups = file_content.split("\n\n")

seeds = [int(x) for x in groups[0][7:].split()]

pairs = []
prev = None
for x in seeds:
    if prev is None:
        prev = x
    else:
        pairs.append((prev, x))
        prev = None


map_source = []
for start, l in pairs:
    for x in range(start, start + l):
        map_source.append(x)

for group in groups[1:]:
    is_mapped = [False] * len(map_source)
    map_destination = map_source[:]
    for mapping in group.split("\n")[1:]:
        dest_start, source_start, range_len = mapping.split()
        dest_start = int(dest_start)
        source_start = int(source_start)
        range_len = int(range_len)
        for i, (x, x_mapped) in enumerate(zip(map_source, is_mapped)):
            if not x_mapped and x >= source_start and x < source_start + range_len:
                map_destination[i] = dest_start + (x - source_start)
                is_mapped[i] = True

    map_source = map_destination[:]

print(min(map_destination))
