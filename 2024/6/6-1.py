import string
import re
import math
from collections import defaultdict
from enum import Enum
import itertools
import tqdm
from dataclasses import dataclass
import random
import os

PRACTICE = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()
lines = file_content.split("\n")

width = len(lines[0])
height = len(lines)


class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


for y, line in enumerate(lines):
    x = line.find("^")
    if x != -1:
        start_position = (x, y)
        break
else:
    raise ("no start position")

visited = set()


@dataclass(frozen=True)
class Node:
    position: tuple[int, int]
    direction: Direction


def step(coord: tuple[int, int], direction: Direction) -> tuple[int, int]:
    x, y = coord
    if direction == Direction.LEFT:
        x -= 1
    elif direction == Direction.RIGHT:
        x += 1

    # NOTE: Python indexing?
    if direction == Direction.DOWN:
        y += 1
    elif direction == Direction.UP:
        y -= 1

    if x < 0 or y < 0 or x >= width or y >= height:
        return None
    return x, y


def get(coord: tuple[int, int]):
    if coord is None:
        return "#"
    return lines[coord[1]][coord[0]]


def turn_right(direction: Direction) -> Direction:
    match direction:
        case Direction.LEFT:
            return Direction.UP
        case Direction.UP:
            return Direction.RIGHT
        case Direction.RIGHT:
            return Direction.DOWN
        case Direction.DOWN:
            return Direction.LEFT


def print_state(node: Node):
    os.system("clear")
    match node.direction:
        case Direction.LEFT:
            dir_char = "<"
        case Direction.UP:
            dir_char = "^"
        case Direction.RIGHT:
            dir_char = ">"
        case Direction.DOWN:
            dir_char = "v"

    x, y = node.position
    for y_printed, line in enumerate(lines):
        if y_printed == y:
            print(line[:x] + dir_char + line[x + 1 :])
        else:
            print(line)
    print()
    input()


current = Node(position=start_position, direction=Direction.UP)

while current not in visited:
    # print_state(current)
    visited.add(current)
    next_position = step(current.position, current.direction)
    next_direction = current.direction

    if next_position is None:
        break  # out of bounds

    while get(next_position) == "#":
        next_direction = turn_right(next_direction)
        next_position = step(current.position, next_direction)
        # print("considering", next_position, next_direction, get(next_position))
    current = Node(position=next_position, direction=next_direction)

print(len(set(n.position for n in visited)))
