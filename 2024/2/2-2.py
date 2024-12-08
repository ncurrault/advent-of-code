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
import numpy as np

PRACTICE = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()
lines = file_content.split("\n")

reports = [[int(x) for x in line.split()] for line in lines]


def is_safe_old(diffs):
    if 0 in diffs:
        return False  # nothing too small
    if any(abs(x) > 3 for x in diffs):
        return False  # nothing too large
    return len(set(x > 0 for x in diffs)) == 1  # monotonic


def is_safe(report):
    diffs = np.diff(report)
    if is_safe_old(diffs):
        return True

    if is_safe_old(diffs[1:]) or is_safe_old(diffs[:-1]):
        return True
    for to_remove in range(1, len(diffs)):
        if is_safe_old(
            [
                *diffs[: to_remove - 1],
                diffs[to_remove - 1] + diffs[to_remove],
                *diffs[to_remove + 1 :],
            ]
        ):
            return True
    return False


print(len([r for r in reports if is_safe(r)]))

# NOTE 651 too low
