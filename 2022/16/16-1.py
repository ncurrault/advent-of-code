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
lines = file_content.split("\n")


# optimization problem
# choice is to *open valve* or *move*
# tree search problem
# can optimize with branch and bound (assuming all other valves open for remaining time)

flow_rates = {}
adjacent_valves = {}

for line in lines:
    parsed = re.findall(
        r"Valve ([A-Z]+) has flow rate=([0-9]+); tunnels? leads? to valves? ((?:[A-Z]+(?:, )?)+)",
        line,
    )
    assert len(parsed) == 1
    valve, flow_rate_str, targets_str = parsed[0]
    flow_rates[valve] = int(flow_rate_str)
    adjacent_valves[valve] = targets_str.split(", ")

# current_valve = "AA"
# current valve, set of open valves, pressure released, remaining time
to_explore = [("AA", set(), 0, 30)]
max_released_so_far = 0


def total_release_upper_bound(valve, open_so_far, released_so_far, remaining_time):
    remaining_flow_rates = sorted(
        (
            flow_rates[v]
            for v in flow_rates
            if v not in open_so_far and flow_rates[v] > 0
        ),
        reverse=True,
    )
    # best case is that we immediately open the best valve, then move to the next best one, etc.
    res = 0
    remaining_time -= 1
    for fr in remaining_flow_rates:
        res += fr * remaining_time
        remaining_time -= 2
        if remaining_time <= 0:
            break
    return released_so_far + res


while len(to_explore) > 0:
    node = to_explore.pop()
    if total_release_upper_bound(*node) < max_released_so_far:
        continue
    valve, open_so_far, released_so_far, remaining_time = node

    remaining_time -= 1  # cost no matter what we do
    if released_so_far > max_released_so_far:
        max_released_so_far = released_so_far
        print(max_released_so_far)
    if remaining_time == 0:
        continue

    for adjacent_valve in adjacent_valves[valve]:
        to_explore.append(
            (adjacent_valve, open_so_far, released_so_far, remaining_time)
        )
    if valve not in open_so_far:
        # try opening valve
        to_explore.append(
            (
                valve,
                open_so_far | {valve},
                released_so_far + (remaining_time * flow_rates[valve]),
                remaining_time,
            )
        )

print(max_released_so_far)
