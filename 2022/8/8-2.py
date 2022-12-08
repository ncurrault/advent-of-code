PRACTICE = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()

lines = file_content.split("\n")
tree_grid = [[int(c) for c in line] for line in lines]

height = len(tree_grid)
width = len(tree_grid[0])


def get_viewing_distance(tree_height, tree_path):
    res = 0
    for t in tree_path:
        res += 1
        if t >= tree_height:
            break
    return res


def get_scenic_score(row, col):
    up_path = [tree_grid[r][col] for r in range(row - 1, -1, -1)]
    down_path = [tree_grid[r][col] for r in range(row + 1, height)]
    left_path = [tree_grid[row][c] for c in range(col - 1, -1, -1)]
    right_path = [tree_grid[row][c] for c in range(col + 1, width)]

    tree_height = tree_grid[row][col]
    return (
        get_viewing_distance(tree_height, up_path)
        * get_viewing_distance(tree_height, down_path)
        * get_viewing_distance(tree_height, left_path)
        * get_viewing_distance(tree_height, right_path)
    )


print(max(get_scenic_score(row, col) for row in range(height) for col in range(width)))
