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


def is_gear(row, col):
    if row < 0 or col < 0 or row >= len(lines) or col >= len(lines[0]):
        return False
    return lines[row][col] == "*"


gears = defaultdict(list)


def add_to_gears(curr_num, row_i, col_i):
    min_col_i = col_i - len(curr_num)
    if is_gear(row_i, min_col_i - 1):
        gears[(row_i, min_col_i - 1)].append(int(curr_num))
    if is_gear(row_i, col_i):
        gears[(row_i, col_i)].append(int(curr_num))
    for col in range(min_col_i - 1, col_i + 1):
        if is_gear(row_i - 1, col):
            gears[(row_i - 1, col)].append(int(curr_num))
        if is_gear(row_i + 1, col):
            print(f"{row_i=} {col=}")
            gears[(row_i + 1, col)].append(int(curr_num))


for row_i, row in enumerate(lines):
    curr_num = ""
    for col_i in range(len(row) + 1):
        cell = row[col_i] if col_i < len(row) else None
        if cell is not None and cell.isdigit():
            curr_num += cell
        elif curr_num != "":
            add_to_gears(curr_num, row_i, col_i)
            curr_num = ""


for gear, nums in gears.items():
    if len(nums) == 2:
        res += (nums[0]) * (nums[1])

print(res)
