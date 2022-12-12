import string
import re
import math
from collections import defaultdict
from priority_queue import PriorityQueue

PRACTICE = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()


# breadth-first search, constrained based on <= +1 elevation criterion
# this time we work backwards: searching for any "a" space starting from E

elevation_grid = []
destination = None
for row_idx, line in enumerate(file_content.split("\n")):
    row = []
    for col_idx, c in enumerate(line):
        if c == "E":
            elevation = "z"
            destination = (row_idx, col_idx)
        else:
            elevation = c
        row.append(elevation)
    elevation_grid.append(row)

height = len(elevation_grid)
width = len(elevation_grid[0])


def in_bounds(row, col):
    return row >= 0 and col >= 0 and row < height and col < width


def valid_steps(row, col):
    current_elevation = elevation_grid[row][col]
    for row_delta in (-1, 0, 1):
        for col_delta in (-1, 0, 1):
            if row_delta == 0 and col_delta == 0:
                continue  # self
            if abs(row_delta) + abs(col_delta) > 1:
                continue  # diagonal
            new_row, new_col = row + row_delta, col + col_delta
            if not in_bounds(new_row, new_col):
                continue

            new_elevation = elevation_grid[new_row][new_col]
            if ord(current_elevation) - ord(new_elevation) <= 1:
                yield (new_row, new_col)


def manhattan_distance(square_a, square_b):
    return abs(square_a[0] - square_b[0]) + abs(square_a[1] - square_b[1])


to_explore = PriorityQueue()
to_explore.add_task((destination, 0))
explored = set()
while True:
    square, steps_so_far = to_explore.pop_task()
    explored.add(square)

    if elevation_grid[square[0]][square[1]] == "a":
        print(f"found path in {steps_so_far} steps!")
        break

    for new_square in valid_steps(*square):
        if new_square not in explored:
            to_explore.add_task(
                (new_square, steps_so_far + 1),
                priority=steps_so_far,
            )
