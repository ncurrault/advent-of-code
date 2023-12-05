import string
import re
import math
from collections import defaultdict
from enum import Enum
import itertools
import tqdm
from dataclasses import dataclass
import random
from copy import copy, deepcopy

PRACTICE = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()
groups = file_content.split("\n\n")


class Intervals:
    sub_intervals: set[tuple[int, int]]

    def __init__(self):
        self.sub_intervals = set()

    def __str__(self):
        return str(self.sub_intervals)

    def update(self, start: int, end: int) -> None:
        if (start, end) in self.sub_intervals:
            return  # interval matches another
        for other_start, other_end in self.sub_intervals:
            if start >= other_start and end <= other_end:
                return  # interval contained within another
        self.sub_intervals.add((start, end))

    def update_obj(self, other: "Intervals") -> None:
        self.sub_intervals.update(other.sub_intervals)

    def contains(self, x: int) -> bool:
        for start, end in self.sub_intervals:
            if x >= start and x <= end:
                return True
        return False

    def subtract(self, start: int, end: int) -> None:
        assert start <= end
        to_remove = []
        to_add = []
        for existing in self.sub_intervals:
            existing_start, existing_end = existing
            if start <= existing_start and existing_end <= end:
                to_remove.append(existing)  # remove whole interval
            elif (
                start <= existing_start and existing_start < end and end <= existing_end
            ):
                # chop off left side: [start][existing start][end][existing end]
                to_remove.append(existing)
                to_add.append((end + 1, existing_end))
            elif (
                existing_start < start and start <= existing_end and existing_end <= end
            ):
                # chop off right side: [existing start][start][existing end][end]
                to_remove.append(existing)
                to_add.append((existing_start, start - 1))
            elif existing_start < start and end < existing_end:
                # remove center
                to_remove.append(existing)
                to_add.append((end + 1, existing_end))
                to_add.append((existing_start, start - 1))

        for i in to_remove:
            self.sub_intervals.remove(i)
        for i in to_add:
            self.sub_intervals.add(i)

    def list_overlaps(self, start: int, end: int):
        res = []
        for existing in self.sub_intervals:
            existing_start, existing_end = existing
            if start <= existing_start and existing_end <= end:
                res.append((existing_start, existing_end))
            elif (
                start <= existing_start and existing_start < end and end <= existing_end
            ):
                res.append((existing_start, end))
            elif (
                existing_start < start and start <= existing_end and existing_end <= end
            ):
                res.append((start, existing_end))
            elif existing_start < start and end < existing_end:
                res.append((start, end))
        return res


seed_ranges = [int(x) for x in groups[0][7:].split()]

map_source_intervals = Intervals()
prev = None
for x in seed_ranges:
    if prev is None:
        prev = x
    else:
        map_source_intervals.update(prev, prev + x - 1)
        prev = None


for group in groups[1:]:
    map_dest_intervals = Intervals()

    for mapping in group.split("\n")[1:]:
        dest_start, source_start, range_len = mapping.split()
        dest_start = int(dest_start)
        source_start = int(source_start)
        range_len = int(range_len)
        source_end = source_start + range_len - 1
        dest_end = dest_start + range_len - 1

        for x_range_start, x_range_end in map_source_intervals.list_overlaps(
            source_start, source_end
        ):
            map_source_intervals.subtract(x_range_start, x_range_end)
            map_dest_intervals.update(
                x_range_start - source_start + dest_start,
                x_range_end - source_start + dest_start,
            )

    map_dest_intervals.update_obj(map_source_intervals)
    map_source_intervals = map_dest_intervals

print(min(x for x, _ in map_source_intervals.sub_intervals))
