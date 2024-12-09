import string
import re
import math
from collections import defaultdict
from enum import Enum
import itertools
from typing import Iterable
from tqdm import tqdm, trange
from dataclasses import dataclass
import random
from copy import deepcopy
import os

PRACTICE = False
DEBUG = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()
lines = file_content.split("\n")

width = len(lines[0])
height = len(lines)

antennas = defaultdict(set)

for y, line in enumerate(lines):
    for x, location in enumerate(line):
        if location in string.ascii_letters + string.digits:
            antennas[location].add((x, y))

antennas = dict(antennas)

antinodes = set()


def get_antinodes(
    antenna_a: tuple[int, int], antenna_b: tuple[int, int]
) -> list[tuple[int, int]]:
    a_x, a_y = antenna_a
    b_x, b_y = antenna_b

    delta_x, delta_y = (a_x - b_x), (a_y - b_y)

    curr_x = a_x
    curr_y = a_y
    while in_bounds((curr_x, curr_y)):
        yield (curr_x, curr_y)
        curr_x += delta_x
        curr_y += delta_y

    curr_x = b_x
    curr_y = b_y
    while in_bounds((curr_x, curr_y)):
        yield (curr_x, curr_y)
        curr_x -= delta_x
        curr_y -= delta_y

    # return [(a_x + delta_x, a_y + delta_y), (b_x - delta_x, b_y - delta_y)]


def get(coord: tuple[int, int]):
    return lines[coord[1]][coord[0]]


def in_bounds(coord: tuple[int, int]):
    x, y = coord
    return x >= 0 and y >= 0 and x < width and y < height


def print_state(antinodes: Iterable[tuple[int, int]]):
    os.system("clear")

    lines_copy = deepcopy(lines)
    for antinode in antinodes:
        obs_x, obs_y = antinode
        lines_copy[obs_y] = (
            lines_copy[obs_y][:obs_x] + "*" + lines_copy[obs_y][obs_x + 1 :]
        )

    print("\n".join(lines_copy))
    print()
    input()


antinodes = set()
for freq_antennas in antennas.values():
    for pair in itertools.combinations(freq_antennas, 2):
        for an in get_antinodes(*pair):
            if in_bounds(an):
                antinodes.add(an)

if DEBUG:
    print_state(antinodes)

print(len(antinodes))
