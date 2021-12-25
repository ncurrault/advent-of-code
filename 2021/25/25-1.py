PRACTICE = False

with open("test.txt" if PRACTICE else "input.txt", "r") as f:
    content = f.read().strip()

grid = [list(row) for row in content.split("\n")]

height = len(grid)
width = len(grid[0])

move_num = 0
while True:
    move_occurred = False
    for i, row in enumerate(grid):
        to_move_east = set()
        for j, cell in enumerate(row):
            if cell != ">":
                continue
            if row[(j + 1) % width] == ".":
                to_move_east.add(j)
        for j in to_move_east:
            row[j], row[(j + 1) % width] = ".", ">"
        move_occurred = move_occurred or len(to_move_east) > 0


    for j in range(width):
        to_move_south = set()
        for i, row in enumerate(grid):
            cell = row[j]
            if cell != "v":
                continue
            if grid[(i + 1) % height][j] == ".":
                to_move_south.add(i)
        for i in to_move_south:
            grid[i][j], grid[(i + 1) % height][j] = ".", "v"
        move_occurred = move_occurred or len(to_move_south) > 0

    move_num += 1
    if not move_occurred:
        break
print(move_num)
