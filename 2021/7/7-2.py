from collections import defaultdict
from math import inf

PRACTICE = False

with open("test.txt" if PRACTICE else "input.txt", "r") as f:
    content = f.read().strip()

state = list(map(int, content.split(",")))

crabs_by_position = defaultdict(int)
for x in state:
    crabs_by_position[x] = state.count(x)

left, right = min(crabs_by_position), max(crabs_by_position)
min_so_far = inf

def tri(n):
    return n * (n + 1) // 2

for x in range(left, right + 1):
    # print(x - 1, left_fuel + right_fuel)
    fuel = sum(
        tri(abs(x - start_pos)) * crabs_by_position[start_pos]
        for start_pos in crabs_by_position
    )

    if fuel < min_so_far:
        min_so_far = fuel

print(min_so_far)
