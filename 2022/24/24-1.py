import string
import re
import math
from collections import defaultdict
from enum import Enum
import itertools
import functools
import tqdm
from dataclasses import dataclass
import random
from priority_queue import PriorityQueue

PRACTICE = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()

lines = file_content.split("\n")[1:-1]


class Direction(Enum):
    NORTHBOUND = (-1, 0)
    SOUTHBOUND = (1, 0)
    EASTBOUND = (0, 1)
    WESTBOUND = (0, -1)

    def __lt__(self, other):
        return self.value[0] < other.value[0] or (
            self.value[0] == other.value[0] and self.value[1] < other.value[1]
        )


DIR_LOOKUP = {
    "v": Direction.SOUTHBOUND,
    ">": Direction.EASTBOUND,
    "<": Direction.WESTBOUND,
    "^": Direction.NORTHBOUND,
}
DIR_REV_LOOKUP = {v: k for k, v in DIR_LOOKUP.items()}


@dataclass(frozen=True)
class Blizzard:
    direction: Direction
    row: int
    col: int

    def __lt__(self, other):
        return (
            self.row < other.row
            or (self.row == other.row and self.col < other.col)
            or (
                self.row == other.row
                and self.col == other.col
                and self.direction < other.direction
            )
        )


valley = []
height = len(lines)
width = len(lines[0]) - 2
for row, line in enumerate(lines):
    for col, c in enumerate(line[1:-1]):
        if c == ".":
            continue
        direction = DIR_LOOKUP[c]
        valley.append(Blizzard(direction=direction, row=row, col=col))

init_valley_state = tuple(sorted(valley))


valley_states = [init_valley_state]


def get_valley_after(num_mins):
    while num_mins >= len(valley_states):
        last_valley_state = valley_states[-1]
        next_valley_state = []
        for b in last_valley_state:
            row_delta, col_delta = b.direction.value
            next_valley_state.append(
                Blizzard(
                    direction=b.direction,
                    row=(b.row + row_delta) % height,
                    col=(b.col + col_delta) % width,
                )
            )
        valley_states.append(tuple(sorted(next_valley_state)))
    return valley_states[num_mins]


def print_blizzards(valley: tuple[Blizzard, ...]):
    blizzards_by_loc = defaultdict(int)
    headings = {}
    for b in valley:
        blizzards_by_loc[(b.row, b.col)] += 1
        headings[(b.row, b.col)] = DIR_REV_LOOKUP[b.direction]

    print("#." + ("#" * width))
    for row in range(height):
        line = "#"
        for col in range(width):
            if blizzards_by_loc[(row, col)] == 0:
                line += "."
            elif blizzards_by_loc[(row, col)] == 1:
                line += headings[(row, col)]
            else:
                line += str(blizzards_by_loc[(row, col)])
        print(line + "#")
    print(("#" * width) + ".#")


@dataclass(frozen=True)
class Node:
    num_mins: int
    row: int
    col: int


# A* search
to_explore = PriorityQueue()
to_explore.add_task(Node(num_mins=1, row=0, col=0))
while True:
    current = to_explore.pop_task()
    if current.row == height - 1 and current.col == width - 1:
        print(current.num_mins + 1)  # need to actually exit
        break

    next_min = current.num_mins + 1
    blizzard_state = get_valley_after(next_min)
    blizzard_locs = set((b.row, b.col) for b in blizzard_state)

    if (current.row, current.col) not in blizzard_locs:
        to_explore.add_task(
            Node(num_mins=next_min, row=current.row, col=current.col),
            priority=next_min + height + width - current.row - current.col,
        )

    for row_delta in (-1, 0, 1):
        new_row = current.row + row_delta
        if new_row < 0 or new_row >= height:
            continue
        for col_delta in (-1, 0, 1):
            if abs(row_delta) + abs(col_delta) != 1:
                continue
            new_col = current.col + col_delta
            if new_col < 0 or new_col >= width:
                continue
            if (new_row, new_col) in blizzard_locs:
                continue
            to_explore.add_task(
                Node(num_mins=next_min, row=new_row, col=new_col),
                priority=next_min + height + width - new_row - new_col,
            )
