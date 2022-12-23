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

grove = [[c == "#" for c in line] for line in lines]

height = len(grove)
width = len(grove[0])

directions = [
    ((0, 1), ((0, 1), (-1, 1), (1, 1))),  # north
    ((0, -1), ((0, -1), (-1, -1), (1, -1))),  # south
    ((-1, 0), ((-1, 0), (-1, -1), (-1, 1))),  # west
    ((1, 0), ((1, 0), (1, -1), (1, 1))),  # east
]


elf_locations = set(
    (col, height - row)
    for row in range(height)
    for col in range(width)
    if grove[row][col]
)


def neighbors(x, y):
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                yield (x + dx, y + dy)


def print_locs(elf_locations):
    min_x = math.inf
    min_y = math.inf
    max_x = -math.inf
    max_y = -math.inf
    for (x, y) in elf_locations:
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
        if x < min_x:
            min_x = x
        if y < min_y:
            min_y = y

    print(
        "\n".join(
            "".join(
                "#" if (x, y) in elf_locations else "." for x in range(min_x, max_x + 1)
            )
            for y in range(max_y, min_y - 1, -1)
        )
    )
    print()


turns = 0
while True:
    turns += 1
    # print_locs(elf_locations)
    proposed_locations = defaultdict(list)
    new_locs = set()
    for (x, y) in elf_locations:
        if all(adjacent_pt not in elf_locations for adjacent_pt in neighbors(x, y)):
            new_locs.add((x, y))
            continue
        for direction, required_empty_deltas in directions:
            required_empty = [(x + dx, y + dy) for dx, dy in required_empty_deltas]
            if not any(pt in elf_locations for pt in required_empty):
                dx, dy = direction
                proposed_locations[(x + dx, y + dy)].append((x, y))
                break
        else:
            new_locs.add((x, y))

    directions = directions[1:] + [directions[0]]
    for loc, origins in proposed_locations.items():
        if len(origins) > 1:
            new_locs.update(origins)
        else:
            new_locs.add(loc)

    if new_locs == elf_locations:
        break
    elf_locations = new_locs

print(turns)
