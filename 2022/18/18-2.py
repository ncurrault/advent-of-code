import string
import re
import math
from collections import defaultdict
from enum import Enum
import itertools
import tqdm
from priority_queue import PriorityQueue

PRACTICE = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()
lines = file_content.split("\n")


def neighbors(cube):
    x, y, z = cube
    yield (x + 1, y, z)
    yield (x - 1, y, z)
    yield (x, y + 1, z)
    yield (x, y - 1, z)
    yield (x, y, z + 1)
    yield (x, y, z - 1)


scan = set([tuple(int(x) for x in line.split(",")) for line in lines])

min_x = min(x for x, y, z in scan)
min_y = min(y for x, y, z in scan)
min_z = min(z for x, y, z in scan)
OUTSIDE_POINT = (min_x - 1, min_y - 1, min_z - 1)
air_pockets = set()
non_air_pockets = {OUTSIDE_POINT}


def manhattan_distance(cube_a, cube_b):
    return (
        abs(cube_a[0] - cube_b[0])
        + abs(cube_a[1] - cube_b[1])
        + abs(cube_a[2] - cube_b[2])
    )


def is_air_pocket(empty_cube):
    """
    A* search to find a point outside of the cube. If found, not air pocket.
    Cache in air_pockets and non_air_pockets. If we find a connection to a point
    in this set, we know the answer without completing the search.
    """
    assert empty_cube not in scan

    if cube in air_pockets:
        return True
    if cube in non_air_pockets:
        return False

    explored = set()
    to_explore = PriorityQueue()
    to_explore.add_task((empty_cube, 0))
    while True:
        try:
            current, steps = to_explore.pop_task()
            if current in explored:
                continue
            if current in air_pockets:
                raise KeyError()
        except KeyError:
            air_pockets.update(explored)
            air_pockets.add(current)
            return True
        if current in non_air_pockets:
            non_air_pockets.update(explored)
            non_air_pockets.add(current)
            return False
        for neighbor in neighbors(current):
            if neighbor in scan:
                continue
            to_explore.add_task(
                (neighbor, steps + 1),
                priority=manhattan_distance(neighbor, OUTSIDE_POINT) + steps,
            )
        explored.add(current)


res = 0

for cube in scan:
    for adjacent_cube in neighbors(cube):
        if adjacent_cube not in scan and not is_air_pocket(adjacent_cube):
            res += 1

print(res)
