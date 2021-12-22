PRACTICE = False

with open("test.txt" if PRACTICE else "input.txt", "r") as f:
    content = f.read().strip()

grid = [ list(map(int, row)) for row in content.split("\n") ]
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

res = 0
for i, row in enumerate(grid):
    for j, val in enumerate(row):
        for other_i, other_j in surroundings(i, j):
            if grid[other_i][other_j] <= val:
                break
        else:
            res += val + 1
print(res)
