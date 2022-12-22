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
CUBE_SIZE = 4 if PRACTICE else 50
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().rstrip()
lines = file_content.split("\n")

board_str, instrs_str = file_content.split("\n\n")

board = board_str.split("\n")
width = max(len(row) for row in board)
height = len(board)
for i, row in enumerate(board):
    board[i] = row + " " * (width - len(row))


@dataclass
class Face:
    left_edge: int
    right_edge: int
    top_edge: int
    bottom_edge: int


faces = []

for border_row in range(0, height, CUBE_SIZE):
    for border_col in range(0, width, CUBE_SIZE):
        if board[border_row][border_col] == " ":
            continue
        faces.append(
            Face(
                left_edge=border_col,
                right_edge=border_col + CUBE_SIZE - 1,
                top_edge=border_row,
                bottom_edge=border_row + CUBE_SIZE - 1,
            )
        )


class FaceSide(str, Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    TOP = "TOP"
    BOTTOM = "BOTTOM"


HEADING_TO_SIDE = [FaceSide.RIGHT, FaceSide.BOTTOM, FaceSide.LEFT, FaceSide.TOP]


@dataclass
class Edge:
    face_from: int
    face_from_side: FaceSide
    face_to: int
    face_to_side: FaceSide


edges = (
    [
        Edge(
            face_from=0,
            face_to=1,
            face_from_side=FaceSide.TOP,
            face_to_side=FaceSide.TOP,
        ),
        Edge(
            face_from=0,
            face_to=2,
            face_from_side=FaceSide.LEFT,
            face_to_side=FaceSide.TOP,
        ),
        Edge(
            face_from=0,
            face_to=5,
            face_from_side=FaceSide.RIGHT,
            face_to_side=FaceSide.RIGHT,
        ),
        Edge(
            face_from=1,
            face_to=5,
            face_from_side=FaceSide.LEFT,
            face_to_side=FaceSide.BOTTOM,
        ),
        Edge(
            face_from=1,
            face_to=4,
            face_from_side=FaceSide.BOTTOM,
            face_to_side=FaceSide.BOTTOM,
        ),
        Edge(
            face_from=2,
            face_to=4,
            face_from_side=FaceSide.BOTTOM,
            face_to_side=FaceSide.LEFT,
        ),
        Edge(
            face_from=3,
            face_to=5,
            face_from_side=FaceSide.RIGHT,
            face_to_side=FaceSide.TOP,
        ),
    ]
    if PRACTICE
    else [
        Edge(
            face_from=0,
            face_from_side=FaceSide.TOP,
            face_to=5,
            face_to_side=FaceSide.LEFT,
        ),
        Edge(
            face_from=0,
            face_from_side=FaceSide.LEFT,
            face_to=3,
            face_to_side=FaceSide.LEFT,
        ),
        Edge(
            face_from=1,
            face_from_side=FaceSide.BOTTOM,
            face_to=2,
            face_to_side=FaceSide.RIGHT,
        ),
        Edge(
            face_from=1,
            face_from_side=FaceSide.RIGHT,
            face_to=4,
            face_to_side=FaceSide.RIGHT,
        ),
        Edge(
            face_from=1,
            face_from_side=FaceSide.TOP,
            face_to=5,
            face_to_side=FaceSide.BOTTOM,
        ),
        Edge(
            face_from=2,
            face_from_side=FaceSide.LEFT,
            face_to=3,
            face_to_side=FaceSide.TOP,
        ),
        Edge(
            face_from=4,
            face_from_side=FaceSide.BOTTOM,
            face_to=5,
            face_to_side=FaceSide.RIGHT,
        ),
    ]
)




# reverse
edges.extend(
    [
        Edge(
            face_from=edge.face_to,
            face_to=edge.face_from,
            face_from_side=edge.face_to_side,
            face_to_side=edge.face_from_side,
        )
        for edge in edges
    ]
)

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


def get_diffs_from_heading(heading):
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
    else:
        raise ValueError()
    return row_diff, col_diff


def get_face_idx(row, col):
    for i, face in enumerate(faces):
        if (
            face.left_edge <= col
            and face.right_edge >= col
            and face.top_edge <= row
            and face.bottom_edge >= row
        ):
            return i
    raise ValueError()


def get_edge(face_idx: int, side: FaceSide):
    for edge in edges:
        if edge.face_from == face_idx and edge.face_from_side == side:
            return edge
    raise ValueError()


def get_position_on_edge(face: Face, side: FaceSide, row: int, col: int):
    if side in {FaceSide.TOP, FaceSide.BOTTOM}:
        return col - face.left_edge
    else:
        return row - face.top_edge


def get_coord_from_pos_on_edge(
    face: Face, side: FaceSide, pos: int, reverse: bool = True
):
    used_pos = CUBE_SIZE - 1 - pos if reverse else pos
    if side == FaceSide.TOP:
        return face.top_edge, face.left_edge + used_pos
    elif side == FaceSide.BOTTOM:
        return face.bottom_edge, face.left_edge + used_pos
    elif side == FaceSide.LEFT:
        return face.top_edge + used_pos, face.left_edge
    elif side == FaceSide.RIGHT:
        return face.top_edge + used_pos, face.right_edge

def should_reverse(side_a, side_b):
    if side_a == side_b:
        return True
    match (side_a, side_b):
        case (FaceSide.TOP, FaceSide.LEFT):
            return False
        case (FaceSide.TOP, FaceSide.RIGHT):
            return True
        case (FaceSide.TOP, FaceSide.BOTTOM):
            return False
        case (FaceSide.LEFT, FaceSide.RIGHT):
            return False
        case (FaceSide.LEFT, FaceSide.BOTTOM):
            return True
        case (FaceSide.RIGHT, FaceSide.BOTTOM):
            return False
        case _:
            return should_reverse(side_b, side_a)


DESTINATION_SIDE_HEADING = {
    FaceSide.LEFT: 0,
    FaceSide.TOP: 1,
    FaceSide.RIGHT: 2,
    FaceSide.BOTTOM: 3,
}

for instr in instrs:
    if DEBUG:
        board_copy[curr_row][curr_col] = ">V<^"[heading]
        print("\n".join("".join(l) for l in board_copy))
        input()

    if instr.isdigit():
        for _ in range(int(instr)):
            row_diff, col_diff = get_diffs_from_heading(heading)
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
                prev_row = curr_row - row_diff
                prev_col = curr_col - col_diff

                prev_face_idx = get_face_idx(prev_row, prev_col)
                prev_face = faces[prev_face_idx]
                side = HEADING_TO_SIDE[heading]
                edge = get_edge(prev_face_idx, side)
                pos = get_position_on_edge(prev_face, side, prev_row, prev_col)
                new_face_idx = edge.face_to
                new_face = faces[new_face_idx]

                reverse = should_reverse(edge.face_from_side, edge.face_to_side)
                other_side_row, other_side_col = get_coord_from_pos_on_edge(
                    new_face, edge.face_to_side, pos, reverse
                )
                other_side_heading = DESTINATION_SIDE_HEADING[edge.face_to_side]

                if board[other_side_row][other_side_col] == "#":
                    curr_row -= row_diff
                    curr_col -= col_diff
                    break
                curr_row = other_side_row
                curr_col = other_side_col
                heading = other_side_heading
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
