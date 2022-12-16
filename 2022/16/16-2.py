import string
import re
import math
from collections import defaultdict
from enum import Enum
import itertools
import random
import tqdm
from dataclasses import dataclass

PRACTICE = True
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
    human_valve, flow_rate_str, targets_str = parsed[0]
    flow_rates[human_valve] = int(flow_rate_str)
    adjacent_valves[human_valve] = targets_str.split(", ")


@dataclass
class Node:
    human_valve: str
    elephant_valve: str
    open_valves: set[str]
    closed_valves: set[str]
    pressure_released: int
    remaining_time: int


def total_release_upper_bound(node: Node):
    remaining_flow_rates = sorted(
        (flow_rates[v] for v in node.closed_valves if flow_rates[v] > 0),
        reverse=True,
    )
    # best case is that we (and elephant) immediately open the two best valves,
    # then move to the next best ones, etc.
    res = node.pressure_released
    if node.remaining_time == 0:
        return node.pressure_released
    remaining_time = node.remaining_time

    if node.human_valve in node.open_valves and node.elephant_valve in node.open_valves:
        remaining_time -= 1
        # both need to move to and open valves that are useful first

    for i in range(0, len(remaining_flow_rates), 2):
        remaining_time -= 1  # open valve
        res += remaining_flow_rates[i] * remaining_time
        if i + 1 < len(remaining_flow_rates):
            res += remaining_flow_rates[i + 1] * remaining_time
        remaining_time -= 1  # move
        if remaining_time <= 0:
            break
    return res


valves = set(v for v in flow_rates)
zero_flow_valves = set(v for v in valves if flow_rates[v] == 0)
# treat 0-flow valves as if they're already open so we don't waste time
# trying to open them

to_explore = [
    Node(
        human_valve="AA",
        elephant_valve="AA",
        open_valves=zero_flow_valves,
        closed_valves=(valves - zero_flow_valves),
        pressure_released=0,
        remaining_time=26,
    )
]
max_released_so_far = 0


while len(to_explore) > 0:
    node = to_explore.pop()
    if total_release_upper_bound(node) <= max_released_so_far:
        continue
    remaining_time = node.remaining_time
    remaining_time -= 1  # cost no matter what we do
    if node.pressure_released > max_released_so_far:
        max_released_so_far = node.pressure_released
        print(max_released_so_far)
    if remaining_time == 0:
        continue

    branch_candidates = []
    # both you and the elephant move
    # by symmetry, it doesn't matter who's at what square
    explored_pairs = set()
    for human_adjacent_valve, elephant_adjacent_valve in itertools.product(
        adjacent_valves[node.human_valve], adjacent_valves[node.elephant_valve]
    ):
        key = tuple(sorted((human_adjacent_valve, elephant_adjacent_valve)))
        if key in explored_pairs:
            continue
        explored_pairs.add(key)
        branch_candidates.append(
            Node(
                human_valve=human_adjacent_valve,
                elephant_valve=elephant_adjacent_valve,
                open_valves=node.open_valves,
                closed_valves=node.closed_valves,
                pressure_released=node.pressure_released,
                remaining_time=remaining_time,
            )
        )

    # you move, elephant opens valve
    if node.elephant_valve in node.closed_valves:
        new_open = node.open_valves | {node.elephant_valve}
        new_closed = node.closed_valves - {node.elephant_valve}
        new_released = node.pressure_released + (
            remaining_time * flow_rates[node.elephant_valve]
        )
        for adjacent_valve in adjacent_valves[node.human_valve]:
            branch_candidates.append(
                Node(
                    human_valve=adjacent_valve,
                    elephant_valve=node.elephant_valve,
                    open_valves=new_open,
                    closed_valves=new_closed,
                    pressure_released=new_released,
                    remaining_time=remaining_time,
                )
            )

    # you open valve, elephant moves
    if (
        node.human_valve in node.closed_valves
        and node.human_valve != node.elephant_valve
    ):
        new_open = node.open_valves | {node.human_valve}
        new_closed = node.closed_valves - {node.human_valve}
        new_released = node.pressure_released + (
            remaining_time * flow_rates[node.human_valve]
        )
        for adjacent_valve in adjacent_valves[node.elephant_valve]:
            branch_candidates.append(
                Node(
                    human_valve=node.human_valve,
                    elephant_valve=adjacent_valve,
                    open_valves=new_open,
                    closed_valves=new_closed,
                    pressure_released=new_released,
                    remaining_time=remaining_time,
                )
            )

    # both open valves
    if (
        node.human_valve in node.closed_valves
        and node.elephant_valve in node.closed_valves
        and node.human_valve != node.elephant_valve
    ):
        new_released = (
            node.pressure_released
            + (remaining_time * flow_rates[node.human_valve])
            + (remaining_time * flow_rates[node.elephant_valve])
        )
        opened_valves = {node.human_valve, node.elephant_valve}
        branch_candidates.append(
            Node(
                human_valve=node.human_valve,
                elephant_valve=node.elephant_valve,
                open_valves=(node.open_valves | opened_valves),
                closed_valves=(node.closed_valves - opened_valves),
                pressure_released=new_released,
                remaining_time=remaining_time,
            )
        )

    branch_candidates_filtered = []
    for n in branch_candidates:
        if total_release_upper_bound(n) > max_released_so_far:
            branch_candidates_filtered.append(n)
    # random.shuffle(branch_candidates_filtered)
    # branch_candidates_filtered
    to_explore += sorted(
        branch_candidates_filtered,
        key=lambda node: node.pressure_released,
    )  # greedy strategy: explore node with most released pressure first

print(max_released_so_far)
