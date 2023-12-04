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


def is_symbol(row, col):
    if row < 0 or col < 0 or row >= len(lines) or col >= len(lines[0]):
        return False
    return not lines[row][col].isdigit() and lines[row][col] != "."


def is_part_num(curr_num, row_i, col_i):
    min_col_i = col_i - len(curr_num)
    if is_symbol(row_i, min_col_i - 1) or is_symbol(row_i, col_i):
        return True
    for col in range(min_col_i - 1, col_i + 1):
        if is_symbol(row_i - 1, col) or is_symbol(row_i + 1, col):
            return True
    return False


for row_i, row in enumerate(lines):
    curr_num = ""
    for col_i in range(len(row) + 1):
        cell = row[col_i] if col_i < len(row) else None
        if cell is not None and cell.isdigit():
            curr_num += cell
        elif curr_num != "":
            if is_part_num(curr_num, row_i, col_i):
                print(row_i, col_i, curr_num)
                res += int(curr_num)
            curr_num = ""

print(res)
