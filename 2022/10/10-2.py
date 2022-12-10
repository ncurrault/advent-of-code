import string
import re
import math
from collections import defaultdict

PRACTICE = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()

lines = file_content.split("\n")

X = 1
crt_position = 1
num_cycles = 0

res = 0


crt_line = ""


def draw_pixel(pixel):
    global crt, crt_line
    crt_line += pixel
    if len(crt_line) == 40:
        print(crt_line)
        crt_line = ""


def update():
    global crt_position, num_cycles
    if crt_position in [X - 1, X, X + 1]:
        pixel = "#"
    else:
        pixel = "."
    draw_pixel(pixel)

    crt_position = (crt_position % 40) + 1
    num_cycles += 1


for line in lines:
    if line == "noop":
        update()
    elif line.startswith("addx"):
        update()
        X += int(line.split()[1])
        update()
    else:
        print("invalid line", line)

print(res)
