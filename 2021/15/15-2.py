from math import inf
from heapq import heappop, heappush
import itertools

PRACTICE = False

with open("test.txt" if PRACTICE else "input.txt", "r") as f:
    content = f.read().strip()

tile = [[int(c) for c in row] for row in content.split("\n")]

tile_height = len(tile)
tile_width = len(tile[0])

height = 5 * tile_height
width = 5 * tile_width

grid = [[None] * width for _ in range(height)]
for tile_i in range(5):
    for tile_j in range(5):
        for small_i in range(tile_height):
            for small_j in range(tile_width):
                val = tile[small_i][small_j] + tile_i + tile_j
                val %= 9
                if val == 0:
                    val = 9
                grid[tile_i * tile_height + small_i][tile_j * tile_width + small_j] = val

# print("\n".join("".join(str(d) for d in row) for row in grid))

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

# source for pq implementation:
# https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes

pq = []                         # list of entries arranged in a heap
entry_finder = {}               # mapping of tasks to entries
REMOVED = '<removed-task>'      # placeholder for a removed task
counter = itertools.count()     # unique sequence count

def add_task(task, priority=0):
    'Add a new task or update the priority of an existing task'
    if task in entry_finder:
        remove_task(task)
    count = next(counter)
    entry = [priority, count, task]
    entry_finder[task] = entry
    heappush(pq, entry)

def remove_task(task):
    'Mark an existing task as REMOVED.  Raise KeyError if not found.'
    entry = entry_finder.pop(task)
    entry[-1] = REMOVED

def pop_task():
    'Remove and return the lowest priority task. Raise KeyError if empty.'
    while pq:
        priority, count, task = heappop(pq)
        if task is not REMOVED:
            del entry_finder[task]
            return task
    raise KeyError('pop from an empty priority queue')

for i in range(height):
    for j in range(width):
        add_task((i, j), distance[i][j])

while distance[-1][-1] == inf:
    i, j = pop_task()

    for new_i, new_j in surroundings(i, j):
        candidate_distance = distance[i][j] + grid[new_i][new_j]
        if candidate_distance < distance[new_i][new_j]:
            distance[new_i][new_j] = candidate_distance
            add_task((new_i, new_j), candidate_distance)
    visited[i][j] = True

print(distance[-1][-1])
