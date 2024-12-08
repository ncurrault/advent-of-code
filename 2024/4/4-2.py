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
data = file_content.split("\n")

width = len(data[0])
height = len(data)
# idea: find all x's, sprawl out for potential searches in each direction


class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"
    NE = "ne"
    NW = "nw"
    SE = "se"
    SW = "sw"


def step(coord, direction):
    x, y = coord
    if direction in (Direction.LEFT, Direction.NW, Direction.SW):
        x -= 1
    elif direction in (Direction.RIGHT, Direction.NE, Direction.SE):
        x += 1

    if direction in (Direction.DOWN, Direction.SE, Direction.SW):
        y -= 1
    elif direction in (Direction.UP, Direction.NE, Direction.NW):
        y += 1

    if x < 0 or y < 0 or x >= width or y >= height:
        return None
    return x, y


def get(coord):
    if coord is None:
        return "*"
    return data[coord[1]][coord[0]]


a_coords = []
for y, row in enumerate(data):
    for x, letter in enumerate(row):
        if letter == "A":
            a_coords.append((x, y))

res = 0


def check(angles):
    if "*" in angles:
        return False
    return (
        angles[0] != angles[2]
        and angles[1] != angles[3]
        and "".join(sorted(set(angles))) == "MS"
    )


for coord in a_coords:
    x_angles = "".join(
        [
            get(step(coord, Direction.NW)),
            get(step(coord, Direction.SW)),
            get(step(coord, Direction.SE)),
            get(step(coord, Direction.NE)),
        ]
    )

    # plus_angles = "".join(
    #     [
    #         get(step(coord, Direction.DOWN)),
    #         get(step(coord, Direction.RIGHT)),
    #         get(step(coord, Direction.UP)),
    #         get(step(coord, Direction.LEFT)),
    #     ]
    # )
    # NOTE: why did I think pluses were ok?

    res += int(check(x_angles))  # + int(check(plus_angles))

print(res)

# NOTE: 1941 too high, and the right answer for another input(!)
