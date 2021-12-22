PRACTICE = False

with open("test.txt" if PRACTICE else "input.txt", "r") as f:
    content = f.read()

x = content.find("\n")
calls = list(map(int, content[:x].split(",")))
board_strs = content[x + 2 :].split("\n\n")
boards = list(
    map(
        lambda board_str: [
            list(map(int, line.split())) for line in board_str.split("\n")
        ],
        board_strs,
    )
)

num_boards = len(boards)
board_maps = [[[False] * 5 for __ in range(5)] for _ in range(num_boards)]

def is_bingo(board_map):
    if [True] * 5 in board_map:
        return True
    for i in range(5):
        for row in board_map:
            if not row[i]:
                break
        else:
            return True
    return False


bingos = set()
last_call = None
last_board = None

for call in calls:
    for i in range(num_boards):
        if i in bingos:
            continue
        for row_idx, row in enumerate(boards[i]):
            if call in row:
                col_idx = row.index(call)
                board_maps[i][row_idx][col_idx] = True
                break
        if is_bingo(board_maps[i]):
            last_call = call
            last_board = i
            bingos.add(i)
    if len(bingos) == num_boards:
        break

sum_unmarked = 0
for row_idx, row in enumerate(boards[last_board]):
    for col_idx, num in enumerate(row):
        if not board_maps[last_board][row_idx][col_idx]:
            sum_unmarked += num
print(sum_unmarked * last_call)
