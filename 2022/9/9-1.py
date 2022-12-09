import string
import re
import math
from collections import defaultdict

PRACTICE = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()

lines = file_content.split("\n")

head_position = [0, 0]
tail_position = [0, 0]


def move(direction):
    match direction:
        case "U":
            head_position[1] += 1
        case "D":
            head_position[1] -= 1
        case "R":
            head_position[0] += 1
        case "L":
            head_position[0] -= 1
        case _:
            print(direction, "invalid")

    x_sign = 0
    y_sign = 0
    if abs(head_position[0] - tail_position[0]) > 1 or abs(head_position[1] - tail_position[1]) > 1:
        if head_position[0] > tail_position[0]:
            x_sign = 1
        elif head_position[0] < tail_position[0]:
            x_sign = -1

        if head_position[1] > tail_position[1]:
            y_sign = 1
        elif head_position[1] < tail_position[1]:
            y_sign = -1

    tail_position[0] += x_sign
    tail_position[1] += y_sign

    assert abs(head_position[0] - tail_position[0]) <= 1
    assert abs(head_position[1] - tail_position[1]) <= 1


tail_positions = {(0, 0)}

for line in lines:
    direction, num_moves = line.split()
    for _ in range(int(num_moves)):
        move(direction)
        tail_positions.add(tuple(tail_position))

print(len(tail_positions))