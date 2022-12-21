import string
import re
import math
from collections import defaultdict
from enum import Enum
import itertools
import tqdm
from dataclasses import dataclass
import random
import sympy

PRACTICE = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()
lines = file_content.split("\n")

known_values = {}
unknown_values = {}

root_deps = []

for line in lines:
    monkey, yell = line.split(": ")
    yell = yell.replace("/", "//")
    if monkey == "humn":
        continue
    if monkey == "root":
        root_deps = [word for word in yell.split() if word.isalpha()]
        continue
    if yell.isdigit():
        known_values[monkey] = int(yell)
    else:
        unknown_values[monkey] = (
            yell,
            [word for word in yell.split() if word.isalpha() and word != "humn"],
        )

humn = sympy.symbols("humn")

while any(wd in unknown_values for wd in root_deps):
    unknown_keys = list(unknown_values.keys())
    for monkey in unknown_keys:
        yell, deps = unknown_values[monkey]
        for x in deps:
            if x in known_values:
                yell = yell.replace(x, f"( {known_values[x]} )")
        new_deps = [dep for dep in deps if dep not in known_values]
        if len(new_deps) == 0:
            if isinstance(eval(yell), int) or isinstance(eval(yell), float):
                yell = eval(yell)
            known_values[monkey] = yell
            del unknown_values[monkey]
        else:
            unknown_values[monkey] = (yell, new_deps)

print(
    sympy.solve(
        f"{known_values[root_deps[0]]} - {known_values[root_deps[1]]}".replace(
            "//", "/"
        )
    )
)
