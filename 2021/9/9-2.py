from functools import reduce

PRACTICE = False

with open("test.txt" if PRACTICE else "input.txt", "r") as f:
    content = f.read().strip()

grid = [list(map(int, row)) for row in content.split("\n")]
height, width = len(grid), len(grid[0])

assert all(len(row) == width for row in grid)


def surroundings(i, j):
    if i > 0:
        yield i - 1, j
    if j > 0:
        yield i, j - 1
    if i < height - 1:
        yield i + 1, j
    if j < width - 1:
        yield i, j + 1


low_points = []
for i, row in enumerate(grid):
    for j, val in enumerate(row):
        for other_i, other_j in surroundings(i, j):
            if grid[other_i][other_j] <= val:
                break
        else:
            low_points.append((i, j))

basins = [set() for _ in low_points]
basin_edges = [{pt} for pt in low_points]
while any(map(lambda s: len(s) > 0, basin_edges)):
    for idx, basin_edge in enumerate(basin_edges):
        basin = basins[idx]
        to_explore = list(basin_edge)
        for i, j in to_explore:
            if (i, j) in basin:
                basin_edge.remove((i, j))
                continue
            for other_i, other_j in surroundings(i, j):
                if grid[other_i][other_j] < 9:
                    basin_edge.add((other_i, other_j))
            basin.add((i, j))
            basin_edge.remove((i, j))

basin_sizes = [len(basin) for basin in basins]
basin_sizes.sort(reverse=True)

print(reduce(lambda a,b: a*b, basin_sizes[:3], 1))
