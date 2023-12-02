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


def check_game(draws):
    for draw in draws:
        for color in draw.split(", "):
            number_str, color = color.split(" ")
            number = int(number_str)
            # 12 red cubes, 13 green cubes, and 14 blue cubes
            if (
                (color == "red" and number > 12)
                or (color == "green" and number > 13)
                or (color == "blue" and number > 14)
            ):
                return False
    return True


res = 0

for i, line in enumerate(lines):
    game_id = i + 1  # line[5 : line.find(":")]
    relevant = line[line.find(":") + 2 :]
    draws = relevant.split("; ")
    if check_game(draws):
        res += game_id

print(res)
