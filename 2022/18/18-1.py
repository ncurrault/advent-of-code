import string
import re
import math
from collections import defaultdict
from enum import Enum
import itertools
import tqdm

PRACTICE = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()
lines = file_content.split("\n")


def neighbors(x, y, z):
    yield (x + 1, y, z)
    yield (x - 1, y, z)
    yield (x, y + 1, z)
    yield (x, y - 1, z)
    yield (x, y, z + 1)
    yield (x, y, z - 1)


scan = set([tuple(int(x) for x in line.split(",")) for line in lines])

res = 0

for cube in scan:
    for adjacent_cube in neighbors(*cube):
        if adjacent_cube not in scan:
            res += 1

print(res)
