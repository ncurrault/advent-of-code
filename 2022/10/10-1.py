import string
import re
import math
from collections import defaultdict

PRACTICE = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()

lines = file_content.split("\n")

X = 1
num_cycles = 0

res = 0


def update_with_signal_strength():
    global res
    if num_cycles % 40 == 20:
        res += num_cycles * X


for line in lines:
    if line == "noop":
        num_cycles += 1
        update_with_signal_strength()
    elif line.startswith("addx"):
        num_cycles += 1
        update_with_signal_strength()
        num_cycles += 1
        update_with_signal_strength()
        X += int(line.split()[1])
    else:
        print("invalid line", line)

print(res)
