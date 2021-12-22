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

num_crabs_at_x = crabs_by_position[left]
left_fuel, right_fuel = 0, sum( (x - left) * crabs_by_position[x] for x in crabs_by_position )
left_crabs, right_crabs = 0, len(state) - num_crabs_at_x

min_so_far = inf

for x in range(left + 1, right + 1):
    # print(x - 1, left_fuel + right_fuel)
    fuel = left_fuel + right_fuel
    if fuel < min_so_far:
        min_so_far = fuel

    left_crabs += num_crabs_at_x
    left_fuel += left_crabs

    num_crabs_at_x = crabs_by_position[x]

    right_fuel -= right_crabs
    right_crabs -= num_crabs_at_x

print(min_so_far)
