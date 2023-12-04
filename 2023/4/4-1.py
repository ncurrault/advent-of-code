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

res = 0

for line in lines:
    line = line[line.find(":") + 2 :]
    winning = line[: line.find(" | ")].split()
    ticket = line[line.find(" | ") + 3 :].split()
    num_overlap = len(set(winning).intersection(set(ticket)))
    if num_overlap == 0:
        continue
    res += 2 ** (num_overlap - 1)

print(res)
