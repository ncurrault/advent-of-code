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


def get_reordered_middle(update: list[int]):
    update_set = set(update)
    relevant_rules = [
        rule for rule in rules if rule[0] in update_set and rule[1] in update_set
    ]

    for x in update_set:
        num_left = len([r for r in relevant_rules if r[1] == x])
        num_right = len([r for r in relevant_rules if r[0] == x])
        if num_left == num_right and num_left > 0:
            return x
    raise Exception()


res = 0

for update in updates:
    if not passes_rules(update):
        res += get_reordered_middle(update)

# INCORRECT: 6418, 6753 is too high

print(res)
