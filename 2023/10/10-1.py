import string
import re
import math
from collections import defaultdict
from enum import Enum
import itertools
import tqdm
from dataclasses import dataclass
import random
from pprint import pprint
from priority_queue import PriorityQueue

PRACTICE = False
with open("test2.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()

# TODO Run Dijkstra's to work way around loop, inserting unexplored coords
# Search graph of pipe, find farthest distance

pipe_layout = [list(row) for row in file_content.split("\n")]
map_height = len(pipe_layout)
map_width = len(pipe_layout[0])

starting_location = None

for i, line in enumerate(pipe_layout):
    if "S" in line:
        starting_location = (i, line.index("S"))


# determine missing pipe at start location
starting_location_row, starting_location_col = starting_location
SOUTH_CONNECTIONS = "|7F"
NORTH_CONNECTIONS = "|LJ"
EAST_CONNECTIONS = "-LF"
WEST_CONNECTIONS = "-J7"

north = "."
if starting_location_row > 0:
    north = pipe_layout[starting_location_row - 1][starting_location_col]
north_has_pipe = north in SOUTH_CONNECTIONS

south = "."
if starting_location_row < map_height - 1:
    south = pipe_layout[starting_location_row + 1][starting_location_col]
south_has_pipe = south in NORTH_CONNECTIONS

east = "."
if starting_location_col < map_width - 1:
    east = pipe_layout[starting_location_row][starting_location_col + 1]
east_has_pipe = east in WEST_CONNECTIONS

west = "."
if starting_location_col > 0:
    west = pipe_layout[starting_location_row][starting_location_col - 1]
west_has_pipe = west in EAST_CONNECTIONS

missing_pipe = None
if north_has_pipe and south_has_pipe:
    missing_pipe = "|"
elif east_has_pipe and west_has_pipe:
    missing_pipe = "-"
elif north_has_pipe and east_has_pipe:
    missing_pipe = "L"
elif north_has_pipe and west_has_pipe:
    missing_pipe = "J"
elif south_has_pipe and west_has_pipe:
    missing_pipe = "7"
elif south_has_pipe and east_has_pipe:
    missing_pipe = "F"

assert missing_pipe is not None
pipe_layout[starting_location_row][starting_location_col] = missing_pipe

# Begin Dijkstra


@dataclass(frozen=True)
class Node:
    row: int
    col: int
    steps_so_far: int


to_explore = PriorityQueue()
to_explore.add_task(
    Node(row=starting_location_row, col=starting_location_col, steps_so_far=0)
)
# NOTE: don't actually need pqueue yet, but preserving just in case part 2 needs it

explored = {}

while True:
    try:
        node = to_explore.pop_task()
    except KeyError:
        break
    pipe = pipe_layout[node.row][node.col]

    explored[(node.row, node.col)] = node.steps_so_far
    adjacent_nodes_to_explore = []

    if pipe in SOUTH_CONNECTIONS:
        adjacent_nodes_to_explore.append((node.row + 1, node.col))
    if pipe in NORTH_CONNECTIONS:
        adjacent_nodes_to_explore.append((node.row - 1, node.col))
    if pipe in EAST_CONNECTIONS:
        adjacent_nodes_to_explore.append((node.row, node.col + 1))
    if pipe in WEST_CONNECTIONS:
        adjacent_nodes_to_explore.append((node.row, node.col - 1))

    for next_node in adjacent_nodes_to_explore:
        if next_node in explored:
            continue
        row, col = next_node

        to_explore.add_task(
            Node(row=row, col=col, steps_so_far=node.steps_so_far + 1),
        )

print(max(explored.values()))
