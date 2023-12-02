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
for line in lines:
    digits = re.sub(r"[^0-9]", "", line)
    res += int(digits[0] + digits[-1])

print(res)
