import string
import re
import math
from collections import defaultdict
from enum import Enum

PRACTICE = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()

TARGET_Y = 10 if PRACTICE else 2000000


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

    def total_size(self, exclude):
        res = set()
        for start, end in self.sub_intervals:
            res.update(range(start, end + 1))
        res.difference_update(exclude)
        return len(res)


def manhattan_distance(square_a, square_b):
    return abs(square_a[0] - square_b[0]) + abs(square_a[1] - square_b[1])


ruled_out = Intervals()
beacons_in_target_line = set()

for line in file_content.split("\n"):
    parsed = re.findall(
        r"Sensor at x=(\-?[0-9]+), y=(\-?[0-9]+): closest beacon is at x=(\-?[0-9]+), y=(\-?[0-9]+)",
        line,
    )
    assert len(parsed) == 1
    assert len(parsed[0]) == 4
    sensor_x, sensor_y, beacon_x, beacon_y = [int(n) for n in parsed[0]]

    if beacon_y == TARGET_Y:
        beacons_in_target_line.add(beacon_x)

    dist = manhattan_distance((sensor_x, sensor_y), (beacon_x, beacon_y))

    dist_to_center = abs(sensor_y - TARGET_Y)
    if dist_to_center > dist:
        continue  # can't rule out anything here
    remaining_dist = dist - dist_to_center
    ruled_out.union(sensor_x - remaining_dist, sensor_x + remaining_dist)

print(ruled_out.total_size(beacons_in_target_line))
