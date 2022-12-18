import string
import re
import math
from collections import defaultdict
from enum import Enum
import itertools
from dataclasses import dataclass
import tqdm

PRACTICE = False
STOPPING_POINT = 1000000000000

with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()

# store rocks as sets of points, normalized to (0, 0) as the bottom-left edge
ROCKS = [
    set([(0, 0), (1, 0), (2, 0), (3, 0)]),
    set([(1, 0), (1, 1), (1, 2), (0, 1), (2, 1)]),
    set([(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]),
    set([(0, 0), (0, 1), (0, 2), (0, 3)]),
    set([(0, 0), (1, 0), (0, 1), (1, 1)]),
]
CHAMBER_WIDTH = 7
chamber = set()


def translate_rock(rock, translation):
    dx, dy = translation
    return set((x + dx, y + dy) for x, y in rock)


def max_occupied_row(chamber):
    if len(chamber) == 0:
        return -1
    return max(y for x, y in chamber)


def print_chamber(chamber, rock):
    chamber_height = max_occupied_row(chamber | rock) + 1
    for y in range(chamber_height - 1, -1, -1):
        row = ""
        for x in range(CHAMBER_WIDTH):
            if (x, y) in rock:
                row += "@"
            elif (x, y) in chamber:
                row += "#"
            else:
                row += "."
        print(f"|{row}|")
    print("+" + ("-" * CHAMBER_WIDTH) + "+")


def rock_is_valid(chamber, rock):
    for pt in rock:
        if pt[1] < 0:
            return False  # under floor
        if pt[0] < 0 or pt[0] >= CHAMBER_WIDTH:
            return False  # outside of walls
        if pt in chamber:
            return False  # overlaps existing rock
    return True


current_rock = None
next_rock_idx = 0
num_rocks_stopped = 0


@dataclass(frozen=True)
class State:
    jet_idx: int
    rock_idx: int
    top_shape: set[int]


@dataclass
class StateResult:
    num_rocks: int
    height: int


seen_states: dict[State, StateResult] = {}
extrapolated_height = None


def get_top_shape(chamber, height):
    empty_row = height
    explored = set()
    to_explore = [(0, empty_row)]
    res = set()
    while len(to_explore) > 0:
        current = to_explore.pop(0)
        if current in explored:
            continue
        explored.add(current)
        x, y = current
        for neighbor in ((x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)):
            neighbor_x, neighbor_y = neighbor
            if neighbor_y > empty_row:
                continue
            if neighbor_x < 0 or neighbor_x >= CHAMBER_WIDTH:
                continue
            if not rock_is_valid(chamber, [neighbor]):
                res.add(neighbor)
                continue
            if neighbor not in explored:
                to_explore.append(neighbor)

    return tuple(sorted(translate_rock(res, (0, -empty_row))))
    # normalize for comparison with much higher equivalent shapes


for jet_idx, jet in itertools.cycle(enumerate(file_content)):
    if current_rock is None:
        current_rock = translate_rock(
            ROCKS[next_rock_idx], (2, max_occupied_row(chamber) + 4)
        )
        next_rock_idx = (next_rock_idx + 1) % len(ROCKS)

    # jet push
    new_rock = translate_rock(current_rock, (1 if jet == ">" else -1, 0))
    if rock_is_valid(chamber, new_rock):
        current_rock = new_rock
    # ignore jet pushes into walls

    # gravity
    new_rock = translate_rock(current_rock, (0, -1))
    if rock_is_valid(chamber, new_rock):
        current_rock = new_rock
    else:
        # if we fell too far, stop here and generate a new rock
        chamber.update(current_rock)
        current_rock = None

        num_rocks_stopped += 1

        height = max_occupied_row(chamber) + 1

        if num_rocks_stopped == STOPPING_POINT:
            print(height + extrapolated_height)
            break

        if extrapolated_height is None:
            state = State(
                jet_idx=jet_idx,
                rock_idx=next_rock_idx,
                top_shape=get_top_shape(chamber, height),
            )
            state_result = StateResult(num_rocks=num_rocks_stopped, height=height)
            if state in seen_states:
                prev_result = seen_states[state]
                height_delta = state_result.height - prev_result.height
                rocks_delta = state_result.num_rocks - prev_result.num_rocks

                num_repeats = (STOPPING_POINT - num_rocks_stopped) // rocks_delta
                extrapolated_height = num_repeats * height_delta
                num_rocks_stopped += num_repeats * rocks_delta
            seen_states[state] = state_result
