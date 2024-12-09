import string
import re
import math
from collections import defaultdict
from enum import Enum
import itertools
from tqdm import tqdm, trange
from dataclasses import dataclass
import random
from copy import deepcopy
import os
from pprint import pprint

PRACTICE = False
DEBUG = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    filesystem_raw = f.read().strip()


class SectorType(Enum):
    FILE = "FILE"
    FREE = "FREE"


@dataclass
class Sector:
    type: SectorType
    size: int
    file_id: int | None = None


# TODO consider other data structures. Binary tree?
# Want pre-sorted list of free sectors by both sizes and locations
sectors: list[Sector] = []
for i, c in enumerate(filesystem_raw):
    current_number = int(c)
    if i % 2 == 0:
        sectors.append(
            Sector(
                type=SectorType.FILE,
                size=current_number,
                file_id=i // 2,
            )
        )
    else:
        sectors.append(Sector(type=SectorType.FREE, size=current_number))


def print_state():
    for sector in sectors:
        if sector.type == SectorType.FREE:
            print("." * sector.size, end="")
        else:
            print(str(sector.file_id) * sector.size, end="")
    print()


currently_moving_sector_idx = len(sectors) - 1

while currently_moving_sector_idx > 0:
    if DEBUG:
        print_state()
        input()
    while sectors[currently_moving_sector_idx].type != SectorType.FILE:
        currently_moving_sector_idx -= 1
    current_file = sectors[currently_moving_sector_idx]

    # search for a new home for this file
    for i in range(len(sectors)):
        if i == currently_moving_sector_idx:
            currently_moving_sector_idx -= 1
            break  # never move a file rightwards; just give up
        if sectors[i].type != SectorType.FREE or sectors[i].size < current_file.size:
            continue
        sectors[i].type = SectorType.FILE
        sectors[i].file_id = current_file.file_id
        if sectors[i].size != current_file.size:  # need to split current sector
            new_sector = Sector(
                type=SectorType.FREE, size=sectors[i].size - current_file.size
            )
            sectors.insert(i + 1, new_sector)
            currently_moving_sector_idx += 1
            sectors[i].size = current_file.size

        current_file.type = SectorType.FREE
        current_file.file_id = None
        currently_moving_sector_idx -= 1
        break  # file successfully moved, can stop searching for target location
    else:
        # found no location for this one, just leave it in place
        currently_moving_sector_idx -= 1

current_idx = 0
res = 0

for sector in sectors:
    if sector.type == SectorType.FREE:
        current_idx += sector.size
    else:
        # i*id + (i+1)*id + (i+2)*id + ...
        # id * (i + (i+1) + (i+2) + ...)
        # n(n+1)/2
        ignore_idx_and_earlier = current_idx - 1
        last_idx = current_idx + sector.size - 1
        indices_sum = (
            last_idx**2 + last_idx - ignore_idx_and_earlier**2 - ignore_idx_and_earlier
        ) // 2

        res += sector.file_id * indices_sum
        current_idx += sector.size

print(res)
