from collections import defaultdict

PRACTICE = False

with open("test.txt" if PRACTICE else "input.txt", "r") as f:
    lines = f.read().strip().split("\n")

def parse_pt(pt_str):
    return tuple(int(x) for x in pt_str.split(","))

def lattice_points(origin, dest):
    if origin[0] > dest[0]:
        origin, dest = dest, origin
    min_x, max_x = min(origin[0], dest[0]), max(origin[0], dest[0])
    min_y, max_y = min(origin[1], dest[1]), max(origin[1], dest[1])
    if origin[0] == dest[0]:
        x = origin[0]
        for y in range(min_y, max_y + 1):
            yield (x, y)
    elif origin[1] == dest[1]:
        y = origin[1]
        for x in range(min_x, max_x + 1):
            yield (x, y)
    elif origin[1] < dest[1]: # up sloping
        for x, y in zip(range(min_x, max_x + 1), range(min_y, max_y + 1)):
            yield (x, y)
    else: # origin[1] > dest[1]
        for x, y in zip(range(min_x, max_x + 1), range(max_y, min_y - 1, -1)):
            yield (x, y)

num_vents = defaultdict(int)
for line in lines:
    origin, dest = map(parse_pt, line.split(" -> "))
    for x, y in lattice_points(origin, dest):
        num_vents[(x, y)] += 1

print([value >= 2 for value in num_vents.values()].count(True))
