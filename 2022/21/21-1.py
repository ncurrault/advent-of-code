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

known_values = {}
unknown_values = {}

for line in lines:
    monkey, yell = line.split(": ")
    if yell.isdigit():
        known_values[monkey] = int(yell)
    else:
        unknown_values[monkey] = (
            yell,
            [word for word in yell.split() if word.isalpha()],
        )

while "root" not in known_values:
    unknown_keys = list(unknown_values.keys())
    for monkey in unknown_keys:
        yell, deps = unknown_values[monkey]
        new_deps = [dep for dep in deps if dep not in known_values]
        if len(new_deps) == 0:
            globals().update(known_values)
            known_values[monkey] = eval(yell)
        else:
            unknown_values[monkey] = (yell, new_deps)

print(known_values["root"])
