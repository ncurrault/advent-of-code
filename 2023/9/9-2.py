import string
import re
import math
from collections import defaultdict
from enum import Enum
import itertools
import tqdm
from dataclasses import dataclass
import random
from pprint import pprint

PRACTICE = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()

histories = [[int(x) for x in line.split()] for line in file_content.split("\n")]


def compute_differences(lst):
    differences = []
    for i in range(len(lst) - 1):
        differences.append(lst[i + 1] - lst[i])
    return differences


result = 0

differences = []
for history in histories:
    differences_triangle = [history]
    while not all(x == 0 for x in differences_triangle[-1]):
        differences_triangle.append(compute_differences(differences_triangle[-1]))

    differences_triangle[-1].insert(0, 0)
    for i in range(len(differences_triangle) - 2, -1, -1):
        differences_triangle[i].insert(
            0, differences_triangle[i][0] - differences_triangle[i + 1][0]
        )

    result += differences_triangle[0][0]

print(result)
