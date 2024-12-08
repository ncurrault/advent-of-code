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

result = 0

# for match in re.findall(r"mul\([0-9][0-9]?[0-9]?,[0-9][0-9]?[0-9]?\)", text):

for match in re.findall(r"mul\([0-9][0-9]?[0-9]?,[0-9][0-9]?[0-9]?\)", file_content):
    print(match)
    result += int(match[4 : match.find(",")]) * int(match[match.find(",") + 1 : -1])

print(result)
