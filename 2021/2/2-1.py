#! /Library/Frameworks/Python.framework/Versions/3.10/bin/python3.10

PRACTICE = False

with open("test.txt" if PRACTICE else "input.txt", "r") as f:
    lines = f.read().strip().split("\n")

horiz, depth = 0, 0
for line in lines:
    [direction, units] = line.split()
    units = int(units)
    match direction:
        case "up":
            depth -= units
        case "down":
            depth += units
        case "forward":
            horiz += units

print(horiz, depth, horiz * depth)
