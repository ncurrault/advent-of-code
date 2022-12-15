import string
import re
import math
from collections import defaultdict
from enum import Enum

PRACTICE = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()


class Intervals:
    def __init__(self):
        self.sub_intervals = set()

    def union(self, start, end):
        if (start, end) in self.sub_intervals:
            return  # interval matches another
        for (other_start, other_end) in self.sub_intervals:
            if start >= other_start and end <= other_end:
                return  # interval contained within another
        self.sub_intervals.add((start, end))

    def contains(self, x):
        for start, end in self.sub_intervals:
            if x >= start and x <= end:
                return True
        return False


# NOTE: the next step would be merging intervals, but that efficiency wasn't necessary to solve


horiz_lines = defaultdict(Intervals)
vertical_lines = defaultdict(Intervals)

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
            vertical_lines[pt1[0]].union(min(pt1[1], pt2[1]), max(pt1[1], pt2[1]))
        else:  # horizontal
            horiz_lines[pt1[1]].union(min(pt1[0], pt2[0]), max(pt1[0], pt2[0]))

floor = lowest_rock + 2

settled_sand = set()


def is_occupied(x, y):
    if y == floor:
        return True
    if (x, y) in settled_sand:
        return True
    if horiz_lines[y].contains(x):
        return True
    if vertical_lines[x].contains(y):
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

    settled_sand.add(sand_grain)
    if sand_grain == (500, 0):
        print(len(settled_sand))
        break
