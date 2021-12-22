from collections import defaultdict
from functools import cache
from math import inf

PRACTICE = False

with open("test.txt" if PRACTICE else "input.txt", "r") as f:
    content = f.read().strip()

grid = [[int(c) for c in row] for row in content.split("\n")]

height = len(grid)
width = len(grid[0])

def surroundings(i, j):
    if i > 0:
        yield i - 1, j
    if j > 0:
        yield i, j - 1
    if i < height - 1:
        yield i + 1, j
    if j < width - 1:
        yield i, j + 1

# only entrances count. so all edegs are just the value they lead towards (digraph)
visited = [[False] * width for _ in range(height)]
distance = [[inf] * width for _ in range(height)]
distance[0][0] = 0

def get_current():
    ret = None
    current_min = inf
    for i in range(height):
        for j in range(width):
            if visited[i][j]:
                continue
            elif distance[i][j] < current_min:
                current_min = distance[i][j]
                ret = (i, j)
    return ret

# TODO dijkstra's alg

while distance[-1][-1] == inf:
    current = get_current()
    if current is None:
        break
    i, j = current

    for new_i, new_j in surroundings(i, j):
        candidate_distance = distance[i][j] + grid[new_i][new_j]
        if candidate_distance < distance[new_i][new_j]:
            distance[new_i][new_j] = candidate_distance
    visited[i][j] = True

print(distance[-1][-1])

# 756 is TOO HIGH
