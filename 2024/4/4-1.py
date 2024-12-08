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
    return data[coord[1]][coord[0]]


x_coords = []
for y, row in enumerate(data):
    for x, letter in enumerate(row):
        if letter == "X":
            x_coords.append((x, y))

res = 0

for coord in x_coords:
    for direction in Direction:
        path = [coord]
        for _ in range(3):
            path.append(step(path[-1], direction))
            if path[-1] is None:
                break
        else:
            if "".join(get(x) for x in path) == "XMAS":
                res += 1

print(res)
