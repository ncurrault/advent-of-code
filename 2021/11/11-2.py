PRACTICE = False

NSTEPS = 100

with open("test.txt" if PRACTICE else "input.txt", "r") as f:
    content = f.read().strip()

energy = [ [int(c) for c in line] for line in content.split("\n") ]
width = len(energy[0])
height = len(energy)

def surroundings(i, j):
    if i > 0:
        yield i - 1, j
    if j > 0:
        yield i, j - 1
    if i < height - 1:
        yield i + 1, j
    if j < width - 1:
        yield i, j + 1

    if i > 0 and j > 0:
        yield i-1, j-1
    if i < height - 1 and j < width - 1:
        yield i+1, j+1
    if i < height - 1 and j > 0:
        yield i+1, j-1
    if i > 0 and j < width - 1:
        yield i-1, j+1

def grid_max(grid):
    return max(map(max, grid))

step = 1
while True:
    for i in range(height):
        for j in range(width):
            energy[i][j] += 1
    flashes = set()

    while grid_max(energy) > 9:
        for i, row in enumerate(energy):
            for j, val in enumerate(row):
                if val <= 9 or (i, j) in flashes:
                    continue
                flashes.add((i, j))
                for other_i, other_j in surroundings(i, j):
                    energy[other_i][other_j] += 1
        for i, j in flashes:
            energy[i][j] = 0
    if len(flashes) == height * width:
        print(step)
        break
    step += 1
