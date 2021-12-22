from collections import defaultdict

PRACTICE = False

with open("test.txt" if PRACTICE else "input.txt", "r") as f:
    content = f.read().strip()

lines = content.split("\n")
point_strs = lines[: lines.index("")]
fold_strs = lines[lines.index("") + 1 :]

points = set( (int(x), int(y)) for x, y in map(lambda s: tuple(s.split(",")), point_strs) )

for fold_str in fold_strs:
    axis = {"x": 0, "y": 1}[ fold_str[len("fold along ")] ]
    val = int( fold_str[fold_str.find("=") + 1:] )
    new_points = set()
    for p in points:
        new_p = list(p)
        if p[axis] > val:
            new_p[axis] -= 2 * (new_p[axis] - val)
        new_points.add(tuple(new_p))
    points = new_points

max_x = max(map(lambda p: p[0], points)) + 1
max_y = max(map(lambda p: p[1], points)) + 1
grid = [["."] * max_x for _ in range(max_y)]
for x, y in points:
    grid[y][x] = "#"
for row in grid:
    print("".join(row))
