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


SNAFU_DIGITS = "=-012"


def _digit_value(c):
    if c.isdigit():
        return int(c)
    elif c == "-":
        return -1
    elif c == "=":
        return -2
    else:
        raise ValueError(c)


def snafu_to_decimal(s):
    res = 0
    for exponent, c in enumerate(s[::-1]):
        res += (5 ** exponent) * _digit_value(c)
    return res


def decimal_to_snafu(n):
    for single_digit in SNAFU_DIGITS:
        if n == _digit_value(single_digit):
            return single_digit

    for last_digit in SNAFU_DIGITS:
        required_val = n - _digit_value(last_digit)
        if required_val % 5 == 0:
            return decimal_to_snafu(required_val // 5) + last_digit
    raise ValueError(n)


res_decimal = 0
for line in lines:
    res_decimal += snafu_to_decimal(line)


print(decimal_to_snafu(res_decimal))
