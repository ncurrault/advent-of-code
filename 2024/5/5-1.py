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

rules_str, updates_str = file_content.split("\n\n")

rules = [[int(x) for x in line.split("|")] for line in rules_str.split("\n")]
updates = [[int(x) for x in line.split(",")] for line in updates_str.split("\n")]


def passes_rules(update: list[int]):
    indices = {x: i for i, x in enumerate(update)}
    for rule in rules:
        first_idx = indices.get(rule[0])
        second_idx = indices.get(rule[1])
        if None not in (first_idx, second_idx) and first_idx > second_idx:
            return False
    return True


res = 0

for update in updates:
    if passes_rules(update):
        res += update[len(update) // 2]

print(res)
