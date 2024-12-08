import string
import re
import math
from collections import defaultdict
from enum import Enum
import itertools
import tqdm
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

    lines_copy = deepcopy(lines)
    if obstacle_location is not None:
        obs_x, obs_y = obstacle_location
        lines_copy[obs_y] = (
            lines_copy[obs_y][:obs_x] + "O" + lines_copy[obs_y][obs_x + 1 :]
        )
    start_x, start_y = start_position
    lines_copy[start_y] = (
        lines_copy[start_y][:start_x] + "." + lines_copy[start_y][start_x + 1 :]
    )

    x, y = node.position
    for y_printed, line in enumerate(lines_copy):
        if y_printed == y:
            print(line[:x] + dir_char + line[x + 1 :])
        else:
            print(line)
    print()
    input()


def obstacle_causes_cycle(obstacle_position: tuple[int, int] | None):
    visited = set()
    current = Node(position=start_position, direction=Direction.UP)

    while current not in visited:
        if DEBUG:
            print_state(current)
        visited.add(current)
        next_position = step(current.position, current.direction)
        next_direction = current.direction

        if next_position is None:
            return False, visited

        while get(next_position) == "#" or next_position == obstacle_position:
            next_direction = turn_right(next_direction)
            next_position = step(current.position, next_direction)
        current = Node(position=next_position, direction=next_direction)

    return True, visited


res = 0

# NOTE: only positions in original path will have an effect
is_cycle, original_path = obstacle_causes_cycle(None)
if is_cycle:
    raise Exception("rethink assumptions, this probably won't happen")
original_path_locations = set(n.position for n in original_path)


for obstacle_location in tqdm.tqdm(original_path_locations):
    if DEBUG:
        print("trying obstacle", obstacle_location)
        input()
    if obstacle_causes_cycle(obstacle_location)[0]:
        res += 1

print(res)
