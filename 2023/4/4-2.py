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


def get_card_num(line):
    return int(line[line.find(" ") + 1 : line.find(":")])


num_won = {get_card_num(line): 1 for line in lines}


for line in lines:
    card_num = get_card_num(line)

    line = line[line.find(":") + 2 :]
    winning = line[: line.find(" | ")].split()
    ticket = line[line.find(" | ") + 3 :].split()
    num_overlap = len(set(winning).intersection(set(ticket)))

    for subseq_card in range(card_num + 1, card_num + num_overlap + 1):
        num_won[subseq_card] += num_won[card_num]

print(sum(num_won.values()))
