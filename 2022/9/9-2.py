import string
import re
import math
from collections import defaultdict

PRACTICE = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()

lines = file_content.split("\n")


NUM_KNOTS = 10
positions = [ [0, 0] for _ in range(NUM_KNOTS) ]

def move_head(direction):
    knot_position = positions[0]
    match direction:
        case "U":
            knot_position[1] += 1
        case "D":
            knot_position[1] -= 1
        case "R":
            knot_position[0] += 1
        case "L":
            knot_position[0] -= 1
        case _:
            print(direction, "invalid")

def update_dependent_knot(knot_moved):
    if knot_moved == len(positions) - 1:
        return # no update necessary

    head_position = positions[knot_moved]
    tail_position = positions[knot_moved + 1]

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
        move_head(direction)
        for knot in range(NUM_KNOTS):
            update_dependent_knot(knot)
        tail_positions.add(tuple(positions[-1]))

print(len(tail_positions))