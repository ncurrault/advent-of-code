import string
import re
import math
from collections import defaultdict
from enum import Enum
import itertools
import tqdm

PRACTICE = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()

MAX_COORD = 20 if PRACTICE else 4000000


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

    # TODO this function is buggy (returns some inaccurate points)
    # but it narrows the search space enough
    def missing_points(self):
        sorted_intervals = sorted(self.sub_intervals, key=lambda x: x[0])
        for i in range(len(sorted_intervals) - 1):
            if sorted_intervals[i][1] + 1 < sorted_intervals[i + 1][0]:
                yield sorted_intervals[i][1] + 1


def manhattan_distance(square_a, square_b):
    return abs(square_a[0] - square_b[0]) + abs(square_a[1] - square_b[1])


beacons = []

for line in file_content.split("\n"):
    parsed = re.findall(
        r"Sensor at x=(\-?[0-9]+), y=(\-?[0-9]+): closest beacon is at x=(\-?[0-9]+), y=(\-?[0-9]+)",
        line,
    )
    assert len(parsed) == 1
    assert len(parsed[0]) == 4
    sensor_x, sensor_y, beacon_x, beacon_y = [int(n) for n in parsed[0]]

    dist = manhattan_distance((sensor_x, sensor_y), (beacon_x, beacon_y))
    beacons.append((sensor_x, sensor_y, dist))


for y in tqdm.trange(MAX_COORD):
    ruled_out = Intervals()
    for sensor_x, sensor_y, dist in beacons:
        dist_to_center = abs(sensor_y - y)
        if dist_to_center > dist:
            continue  # can't rule out anything here
        remaining_dist = dist - dist_to_center
        ruled_out.union(sensor_x - remaining_dist, sensor_x + remaining_dist)
    for x in ruled_out.missing_points():
        if any(
            manhattan_distance((x, y), (sensor_x, sensor_y)) <= dist
            for sensor_x, sensor_y, dist in beacons
        ):
            continue
        print(x, y, x * 4000000 + y)
