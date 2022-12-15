import string
import re
import math
from collections import defaultdict
from enum import Enum

PRACTICE = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()


horiz_lines = defaultdict(list)
vertical_lines = defaultdict(list)

lowest_rock = -math.inf

for line in file_content.split("\n"):
    points = []
    for point_str in line.split(" -> "):
        x, y = point_str.split(",")
        points.append((int(x), int(y)))
    for i in range(len(points) - 1):
        pt1 = points[i]
        pt2 = points[i + 1]
        lowest_rock = max(pt1[1], pt2[1], lowest_rock)
        if pt1[0] == pt2[0]:  # vertical
            vertical_lines[pt1[0]].append((min(pt1[1], pt2[1]), max(pt1[1], pt2[1])))
        else:  # horizontal
            horiz_lines[pt1[1]].append((min(pt1[0], pt2[0]), max(pt1[0], pt2[0])))
        # TODO improve efficiency by merging intervals

settled_sand = set()


def is_occupied(x, y):
    if (x, y) in settled_sand:
        return True
    for hl in horiz_lines[y]:
        if x >= hl[0] and x <= hl[1]:
            return True
    for vl in vertical_lines[x]:
        if y >= vl[0] and y <= vl[1]:
            return True
    return False


def sand_fall(x, y):
    for candidate in [(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)]:
        if not is_occupied(*candidate):
            return candidate
    return None


while True:
    next_position = (500, 0)
    while next_position is not None:
        sand_grain = next_position
        next_position = sand_fall(*sand_grain)
        if next_position is not None and next_position[1] > lowest_rock:
            print("solution:", len(settled_sand))
            break
    else:
        settled_sand.add(sand_grain)
        continue
    break
