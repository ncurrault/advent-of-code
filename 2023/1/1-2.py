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
with open("test2.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()
lines = file_content.split("\n")

NUMBERS = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]

res = 0
for line in lines:
    digits = re.sub(r"[^0-9]", "", line)

    first_digit = digits[0] if len(digits) > 0 else None
    last_digit = digits[-1] if len(digits) > 0 else None

    first_digit_loc = line.find(first_digit) if first_digit is not None else len(line)
    last_digit_loc = line.rfind(last_digit) if first_digit is not None else 0

    for i in range(first_digit_loc):
        for other_digit, other_digit_str in enumerate(NUMBERS):
            if i + len(other_digit_str) > first_digit_loc:
                continue
            if line[i:].startswith(other_digit_str):
                first_digit = other_digit
                break
        else:
            continue
        break

    for i in range(len(line) - 1, last_digit_loc, -1):
        for other_digit, other_digit_str in enumerate(NUMBERS):
            if i + len(other_digit_str) > len(line):
                continue
            if line[i:].startswith(other_digit_str):
                last_digit = other_digit
                break
        else:
            continue
        break

    res += int(str(first_digit) + str(last_digit))


print(res)
