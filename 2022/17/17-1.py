import string
import re
import math
from collections import defaultdict
from enum import Enum
import itertools
import tqdm

PRACTICE = False
DEBUG = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()

# store rocks as sets of points, normalized to (0, 0) as the bottom-left edge
ROCKS = [
    set([(0, 0), (1, 0), (2, 0), (3, 0)]),
    set([(1, 0), (1, 1), (1, 2), (0, 1), (2, 1)]),
    set([(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]),
    set([(0, 0), (0, 1), (0, 2), (0, 3)]),
    set([(0, 0), (1, 0), (0, 1), (1, 1)]),
]
CHAMBER_WIDTH = 7
chamber = set()


def translate_rock(rock, translation):
    dx, dy = translation
    return set((x + dx, y + dy) for x, y in rock)


def max_occupied_row(chamber):
    if len(chamber) == 0:
        return -1
    return max(y for x, y in chamber)


def print_chamber(chamber, rock):
    chamber_height = max_occupied_row(chamber | rock) + 1
    for i in range(chamber_height - 1, -1, -1):
        row = ""
        for j in range(CHAMBER_WIDTH):
            if (i, j) in chamber:
                row += "#"
            elif (i, j) in rock:
                row += "@"
            else:
                row += "."
        print(f"|{row}|")
    print("+" + ("-" * CHAMBER_WIDTH) + "+")


def rock_is_valid(chamber, rock):
    for pt in rock:
        if pt[1] < 0:
            return False  # under floor
        if pt[0] < 0 or pt[0] >= CHAMBER_WIDTH:
            return False  # outside of walls
        if pt in chamber:
            return False  # overlaps existing rock
    return True


current_rock = None
next_rock_idx = 0
num_rocks_stopped = 0

for jet in itertools.cycle(file_content):
    if current_rock is None:
        current_rock = translate_rock(
            ROCKS[next_rock_idx], (2, max_occupied_row(chamber) + 4)
        )
        next_rock_idx = (next_rock_idx + 1) % len(ROCKS)

    if DEBUG:
        print_chamber(chamber, current_rock)
        print()

    # jet push
    new_rock = translate_rock(current_rock, (1 if jet == ">" else -1, 0))
    if rock_is_valid(chamber, new_rock):
        current_rock = new_rock
    # ignore jet pushes into walls

    if DEBUG:
        print(f"{jet=}")
        print_chamber(chamber, current_rock)

    # gravity
    new_rock = translate_rock(current_rock, (0, -1))
    if rock_is_valid(chamber, new_rock):
        current_rock = new_rock
    else:
        # if we fell too far, stop here and generate a new rock
        chamber.update(current_rock)
        current_rock = None

        num_rocks_stopped += 1
        if num_rocks_stopped == 2022:
            break

print(max_occupied_row(chamber) + 1)
