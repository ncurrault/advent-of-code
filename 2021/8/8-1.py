from collections import defaultdict
from math import inf

PRACTICE = False

key = [
    "abcefg",  # 0
    "cf",      # 1-
    "acdeg",   # 2
    "acdfg",   # 3
    "bcdf",    # 4-
    "abdfg",   # 5
    "abdefg",  # 6
    "acf",     # 7-
    "abcdefg", # 8-
    "abcdfg"   # 9
]
# 1, 4, 7, 8 all have unique lengths...


with open("test.txt" if PRACTICE else "input.txt", "r") as f:
    content = f.read().strip()

lines = content.split("\n")
res = 0
for line in lines:
    training_str, code_str = line.split(" | ")
    code = code_str.split()
    for digit in code:
        if len(digit) in map(lambda x: len(key[x]), (1, 4, 7, 8)):
            res += 1

print(res)
