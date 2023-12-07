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

time = int("".join(lines[0].split()[1:]))
distance = int("".join(lines[1].split()[1:]))


# (t - hold_period) * hold_period > d
# t h - h^2 > d
# want difference between roots (rounded inwards)
# - h^2 + t h - d = 0
# h = [-t +/- sqrt(t^2 - 4 (-1) (-d))] / (-2)
# h = [t +/- sqrt(t^2 - 4d)] / 2

pos_root = (time + math.sqrt(time**2 - 4 * distance)) / 2
neg_root = (time - math.sqrt(time**2 - 4 * distance)) / 2

min_holding = int(math.ceil(min(pos_root, neg_root)))
max_holding = int(math.floor(max(pos_root, neg_root)))


print(max_holding - min_holding + 1)
