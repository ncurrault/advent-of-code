import string
import re
import math
from collections import defaultdict
from enum import Enum

PRACTICE = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()


class ComparisonResult(Enum):
    LESS_THAN = -1
    EQUAL_TO = 0
    GREATER_THAN = 1


def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return ComparisonResult.LESS_THAN
        if left > right:
            return ComparisonResult.GREATER_THAN
        else:
            return ComparisonResult.EQUAL_TO
    if isinstance(left, list) and isinstance(right, list):
        for i in range(min(len(left), len(right))):
            item_compare = compare(left[i], right[i])
            if item_compare != ComparisonResult.EQUAL_TO:
                return item_compare

        if len(left) < len(right):
            return ComparisonResult.LESS_THAN
        elif len(left) > len(right):
            return ComparisonResult.GREATER_THAN
        else:
            return ComparisonResult.EQUAL_TO

    if isinstance(left, int):
        return compare([left], right)
    if isinstance(right, int):
        return compare(left, [right])

    raise ValueError(f"could not compare {left} and {right}")


res = 0

pair_strs = file_content.split("\n\n")
for idx, pair_str in enumerate(pair_strs):
    left_str, right_str = pair_str.split("\n")
    left = eval(left_str)
    right = eval(right_str)
    if compare(left, right) != ComparisonResult.GREATER_THAN:
        res += idx + 1

print(res)
