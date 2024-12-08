import string
import re
import math
from collections import defaultdict
from enum import Enum
import itertools
from typing import Iterable
from tqdm import tqdm, trange
from dataclasses import dataclass
import random
from copy import deepcopy
import os

PRACTICE = False
DEBUG = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()
lines = file_content.split("\n")


class Operator(Enum):
    PLUS = "PLUS"
    TIMES = "TIMES"
    CONCAT = "CONCAT"


def eval(nums: list[int], ops: Iterable[Operator], test_value: int):
    assert len(nums) == len(ops) + 1
    current = nums[0]
    for next_num, op in zip(nums[1:], ops):
        if current > test_value:
            return None  # cannot possibly match
        match op:
            case Operator.PLUS:
                current += next_num
            case Operator.TIMES:
                current *= next_num
            case Operator.CONCAT:
                current = int(str(current) + str(next_num))
    return current == test_value


res = 0

for line in tqdm(lines):
    test_value_str, nums_str = line.split(": ")
    test_value = int(test_value_str)
    nums = [int(n) for n in nums_str.split()]

    for ops in itertools.product(
        [Operator.PLUS, Operator.TIMES, Operator.CONCAT], repeat=len(nums) - 1
    ):
        if eval(nums, ops, test_value):
            res += test_value
            break


print(res)
