import math

PRACTICE = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()

lines = file_content.split("\n")
tree_grid = [[int(c) for c in line] for line in lines]

height = len(tree_grid)
width = len(tree_grid[0])

is_visible_from_horizontals = []

for row in range(height):
    max_so_far = -math.inf
    visible_from_left = []
    for col in range(width):
        current = tree_grid[row][col]
        visible_from_left.append(current > max_so_far)
        max_so_far = max(max_so_far, current)

    max_so_far = -math.inf
    visible_from_right = []
    for col in range(width - 1, -1, -1):
        current = tree_grid[row][col]
        visible_from_right.append(current > max_so_far)
        max_so_far = max(max_so_far, current)
    visible_from_right = visible_from_right[::-1]

    is_visible_from_horizontals.append(
        [visible_from_left[i] or visible_from_right[i] for i in range(width)]
    )

is_visible_from_verticals = [[] for _ in range(height)]
for col in range(width):
    max_so_far = -math.inf
    visible_from_top = []
    for row in range(height):
        current = tree_grid[row][col]
        visible_from_top.append(current > max_so_far)
        max_so_far = max(max_so_far, current)

    max_so_far = -math.inf
    visible_from_bottom = []
    for row in range(height - 1, -1, -1):
        current = tree_grid[row][col]
        visible_from_bottom.append(current > max_so_far)
        max_so_far = max(max_so_far, current)
    visible_from_bottom = visible_from_bottom[::-1]

    for row in range(height):
        is_visible_from_verticals[row].append(
            visible_from_top[row] or visible_from_bottom[row]
        )

res = 0
for row in range(height):
    for col in range(width):
        res += int(
            is_visible_from_horizontals[row][col] or is_visible_from_verticals[row][col]
        )

print(res)
