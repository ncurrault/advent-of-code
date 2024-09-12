import string
import re
import math
from collections import defaultdict
from enum import Enum
import itertools
import tqdm
from dataclasses import dataclass, field
import random

PRACTICE = False
with open("test2.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()
directions, lines_str = file_content.split("\n\n")


@dataclass(frozen=True, kw_only=True)
class State:
    node: str
    direction_index: int


network = {}
for line in lines_str.split("\n"):
    network[line[:3]] = (line[7:10], line[12:-1])

start_nodes = [node for node in network if node.endswith("A")]
histories = [
    [State(node=node, direction_index=len(directions) - 1)] for node in start_nodes
]
history_sets = [set(h) for h in histories]
remaining_indices = set(range(len(start_nodes)))

num_steps = 0

while True:
    for dir_i, d in enumerate(directions):
        to_remove = set()
        for i in remaining_indices:
            curr = histories[i][-1].node
            next = network[curr][int(d == "R")]
            new_state = State(node=next, direction_index=dir_i)
            histories[i].append(new_state)
            if new_state in history_sets[i]:
                to_remove.add(i)
            else:
                history_sets[i].add(new_state)
        remaining_indices.difference_update(to_remove)
        if len(remaining_indices) == 0:
            break
    else:
        continue
    break

print("computed cycles")
# TODO "rotate" cycles to point where they're all in the cycle, take instances of --Z, LCM of possible LCMs


@dataclass
class CycleDescription:
    offset: int
    cycle_length: int
    ending_node_idx: int

    current_step: int
    valid_final_steps: set[int]


cycle_descriptions: list[CycleDescription] = []

for history in histories:
    offset = history.index(history[-1])
    cycle_length = len(history) - offset - 1
    # [1, 2, 3, 4, 5, 3] [4, 5, 3, 4, 5, 3] offset 2 cycle 3

    ending_nodes = []
    for i, node in enumerate(history):
        if node.node.endswith("Z"):
            ending_nodes.append(i)

    assert len(ending_nodes) == 1
    assert all(i > offset for i in ending_nodes)
    # happened to notice this in example data, greatly simplifies computation

    ending_node_idx = ending_nodes[0]

    desc = CycleDescription(
        offset=offset,
        cycle_length=cycle_length,
        ending_node_idx=ending_node_idx,
        current_step=ending_node_idx,
        valid_final_steps={ending_node_idx},
    )
    cycle_descriptions.append(desc)


lcm = 1
for c in cycle_descriptions:
    lcm = math.lcm(lcm, c.cycle_length)

print(lcm)
# TODO: weird that offsets did not impact... but it works
