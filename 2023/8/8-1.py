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
directions, lines_str = file_content.split("\n\n")


network = {}
for line in lines_str.split("\n"):
    network[line[:3]] = (line[7:10], line[12:-1])

curr_node = "AAA"
num_steps = 0

while True:
    for d in directions:
        curr_node = network[curr_node][int(d == "R")]
        num_steps += 1
        if curr_node == "ZZZ":
            print(num_steps)
            break
    else:
        continue
    break
