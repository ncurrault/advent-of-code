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

CARDS = "23456789TJQKA"


def hand_type(hand):
    num_occurrences = [hand.count(card) for card in CARDS]
    num_occurrences_set = set(num_occurrences)
    if 5 in num_occurrences_set:
        return 7
    elif 4 in num_occurrences_set:
        return 6
    elif 2 in num_occurrences_set and 3 in num_occurrences_set:
        return 5
    elif 3 in num_occurrences_set:
        return 4
    elif num_occurrences.count(2) == 2:
        return 3
    elif 2 in num_occurrences:
        return 2
    else:
        assert len(hand) == len(set(hand))
        return 1


def hand_value_key(hand):
    return (hand_type(hand), *(CARDS.index(x) for x in hand))


hands = []
for line in lines:
    hand, bid = line.split()
    hands.append((hand, int(bid)))

hands.sort(key=lambda x: hand_value_key(x[0]))

res = 0
for rank, (hand, bid) in enumerate(hands):
    res += (rank + 1) * bid

print(res)
