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
DEBUG = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().rstrip()
lines = file_content.split("\n")

board_str, instrs_str = file_content.split("\n\n")

board = board_str.split("\n")
width = max(len(row) for row in board)
height = len(board)
for i, row in enumerate(board):
    board[i] = row + " " * (width - len(row))


curr_row = 0
curr_col = 0
while board[curr_row][curr_col] == " ":
    curr_col += 1

# right, down, left, up
heading = 0

if DEBUG:
    board_copy = [list(l) for l in board]

instrs = []

current_instr = instrs_str[0]
for i, c in enumerate(instrs_str):
    if current_instr.isdigit() != c.isdigit():
        instrs.append(current_instr)
        current_instr = ""
    current_instr += c
instrs.append(current_instr)

for instr in instrs:
    if DEBUG:
        board_copy[curr_row][curr_col] = ">V<^"[heading]
        print("\n".join("".join(l) for l in board_copy))
        input()

    if instr.isdigit():
        if heading == 0:
            row_diff = 0
            col_diff = 1
        elif heading == 1:
            row_diff = 1
            col_diff = 0
        elif heading == 2:
            row_diff = 0
            col_diff = -1
        elif heading == 3:
            row_diff = -1
            col_diff = 0
        for _ in range(int(instr)):
            if DEBUG:
                board_copy[curr_row][curr_col] = ">V<^"[heading]
            curr_row += row_diff
            curr_col += col_diff
            if (
                curr_row < 0
                or curr_col < 0
                or curr_row >= height
                or curr_col >= width
                or board[curr_row][curr_col] == " "
            ):
                other_side_row = curr_row % height
                other_side_col = curr_col % width
                while board[other_side_row][other_side_col] == " ":
                    other_side_row = (other_side_row + row_diff) % height
                    other_side_col = (other_side_col + col_diff) % width
                if board[other_side_row][other_side_col] == "#":
                    curr_row -= row_diff
                    curr_col -= col_diff
                    break
                curr_row = other_side_row
                curr_col = other_side_col
            if board[curr_row][curr_col] == "#":
                curr_row -= row_diff
                curr_col -= col_diff
                break

    else:
        if instr == "R":
            heading = (heading + 1) % 4
        else:
            heading = (heading - 1) % 4

print(1000 * (curr_row + 1) + 4 * (curr_col + 1) + heading)

if DEBUG:
    print(f"{curr_row=} {curr_col=} {heading=}")
    print("\n".join("".join(l) for l in board_copy))
