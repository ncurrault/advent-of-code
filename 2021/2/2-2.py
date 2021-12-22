#! /Library/Frameworks/Python.framework/Versions/3.10/bin/python3.10

PRACTICE = True

with open("test.txt" if PRACTICE else "input.txt", "r") as f:
    lines = f.read().strip().split("\n")

horiz, depth, aim = 0, 0, 0
for line in lines:
    [direction, x] = line.split()
    x = int(x)
    match direction:
        case "up":
            aim -= x
        case "down":
            aim += x
        case "forward":
            horiz += x
            depth += x * aim

print(horiz, depth, horiz * depth)
