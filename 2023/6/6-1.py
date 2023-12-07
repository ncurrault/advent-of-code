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

times = [int(x) for x in lines[0].split()[1:]]
distances = [int(x) for x in lines[1].split()[1:]]

res = 1

for t, d in zip(times, distances):
    num_win_conditions = 0
    for hold_period in range(1, t):
        dist_travelled = (t - hold_period) * hold_period
        if dist_travelled > d:
            num_win_conditions += 1
    res *= num_win_conditions

print(res)
