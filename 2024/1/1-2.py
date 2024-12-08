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

left = []
right = []

for line in lines:
    l_entry, r_entry = line.split()
    left.append(int(l_entry))
    right.append(int(r_entry))


print(sum(x * right.count(x) for x in left))
