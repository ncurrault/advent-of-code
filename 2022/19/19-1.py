import string
import re
import math
from collections import defaultdict
from enum import Enum
import itertools
import tqdm
from dataclasses import dataclass
import random

PRACTICE = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()
lines = file_content.split("\n")


# optimization problem
# choice is to *make a robot* and if so *what type*
# tree search problem
# can optimize with branch and bound


@dataclass
class Blueprint:
    ore_robot_ore: int
    clay_robot_ore: int
    obsidian_robot_ore: int
    obsidian_robot_clay: int
    geode_robot_ore: int
    geode_robot_obsidian: int


blueprints: dict[int, Blueprint] = {}

for line in lines:
    parsed = re.findall(
        r"Blueprint ([0-9]+): Each ore robot costs ([0-9]+) ore. Each clay robot costs ([0-9]+) ore. Each obsidian robot costs ([0-9]+) ore and ([0-9]+) clay. Each geode robot costs ([0-9]+) ore and ([0-9]+) obsidian.",
        line,
    )
    assert len(parsed) == 1
    (
        blueprint_id,
        ore_cost,
        clay_cost,
        obs_cost_ore,
        obs_cost_clay,
        geode_cost_ore,
        geode_cost_obsidian,
    ) = parsed[0]

    blueprints[int(blueprint_id)] = Blueprint(
        ore_robot_ore=int(ore_cost),
        clay_robot_ore=int(clay_cost),
        obsidian_robot_ore=int(obs_cost_ore),
        obsidian_robot_clay=int(obs_cost_clay),
        geode_robot_ore=int(geode_cost_ore),
        geode_robot_obsidian=int(geode_cost_obsidian),
    )


@dataclass
class Node:
    ore: int
    clay: int
    obsidian: int
    geode: int
    ore_robots: int
    clay_robots: int
    obsidian_robots: int
    geode_robots: int
    remaining_time: int


def geodes_upper_bound(node: Node):
    res = node.geode
    remaining_time = node.remaining_time
    while remaining_time > 0:
        remaining_time -= 1
        res += remaining_time
    return res


TOTAL_TIME = 24

res = 0

for bp_id, blueprint in blueprints.items():
    max_ore_robots = max(
        blueprint.ore_robot_ore, blueprint.clay_robot_ore, blueprint.geode_robot_ore
    )
    max_clay_robots = blueprint.obsidian_robot_clay
    max_obsidian_robots = blueprint.geode_robot_obsidian

    max_so_far = 0
    to_explore = [
        Node(
            ore=0,
            clay=0,
            obsidian=0,
            geode=0,
            ore_robots=1,
            clay_robots=0,
            obsidian_robots=0,
            geode_robots=0,
            remaining_time=TOTAL_TIME,
        )
    ]

    while len(to_explore) > 0:
        node = to_explore.pop()
        if geodes_upper_bound(node) <= max_so_far:
            continue

        if node.geode > max_so_far:
            max_so_far = node.geode
        if node.remaining_time == 0:
            continue

        base_node = Node(
            ore=node.ore + node.ore_robots,
            clay=node.clay + node.clay_robots,
            obsidian=node.obsidian + node.obsidian_robots,
            geode=node.geode,
            ore_robots=node.ore_robots,
            clay_robots=node.clay_robots,
            obsidian_robots=node.obsidian_robots,
            geode_robots=node.geode_robots,
            remaining_time=(node.remaining_time - 1),
        )

        # *always* make a geode robot if we can afford one
        if (
            node.ore >= blueprint.geode_robot_ore
            and node.obsidian >= blueprint.geode_robot_obsidian
        ):
            to_explore.append(
                Node(
                    ore=base_node.ore - blueprint.geode_robot_ore,
                    clay=base_node.clay,
                    obsidian=base_node.obsidian - blueprint.geode_robot_obsidian,
                    geode=base_node.geode + base_node.remaining_time,
                    ore_robots=base_node.ore_robots,
                    clay_robots=base_node.clay_robots,
                    obsidian_robots=base_node.obsidian_robots,
                    geode_robots=base_node.geode_robots + 1,
                    remaining_time=base_node.remaining_time,
                )
            )
            continue

        # if not, we can build another robot or just wait
        candidates = []

        if node.ore >= blueprint.ore_robot_ore and node.ore_robots < max_ore_robots:
            candidates.append(
                Node(
                    ore=base_node.ore - blueprint.ore_robot_ore,
                    clay=base_node.clay,
                    obsidian=base_node.obsidian,
                    geode=base_node.geode,
                    ore_robots=base_node.ore_robots + 1,
                    clay_robots=base_node.clay_robots,
                    obsidian_robots=base_node.obsidian_robots,
                    geode_robots=base_node.geode_robots,
                    remaining_time=base_node.remaining_time,
                )
            )
        if node.ore >= blueprint.clay_robot_ore and node.clay_robots < max_clay_robots:
            candidates.append(
                Node(
                    ore=base_node.ore - blueprint.clay_robot_ore,
                    clay=base_node.clay,
                    obsidian=base_node.obsidian,
                    geode=base_node.geode,
                    ore_robots=base_node.ore_robots,
                    clay_robots=base_node.clay_robots + 1,
                    obsidian_robots=base_node.obsidian_robots,
                    geode_robots=base_node.geode_robots,
                    remaining_time=base_node.remaining_time,
                )
            )
        if (
            node.ore >= blueprint.obsidian_robot_ore
            and node.clay >= blueprint.obsidian_robot_clay
            and node.obsidian_robots < max_obsidian_robots
        ):
            candidates.append(
                Node(
                    ore=base_node.ore - blueprint.obsidian_robot_ore,
                    clay=base_node.clay - blueprint.obsidian_robot_clay,
                    obsidian=base_node.obsidian,
                    geode=base_node.geode,
                    ore_robots=base_node.ore_robots,
                    clay_robots=base_node.clay_robots,
                    obsidian_robots=base_node.obsidian_robots + 1,
                    geode_robots=base_node.geode_robots,
                    remaining_time=base_node.remaining_time,
                )
            )

        # no point waiting if we have materials to make everything
        if len(candidates) < 3:
            to_explore.append(base_node)
        random.shuffle(candidates)
        to_explore.extend(candidates)

    score = bp_id * max_so_far
    res += score
    print(f"{bp_id=}, {max_so_far=}, {score=}")

print(res)
