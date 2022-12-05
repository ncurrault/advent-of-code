import re

PRACTICE = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read()


N_STACKS = 3 if PRACTICE else 9


lines = file_content.split("\n")

crate_lines = []
move_lines = []
for line in lines:
    if line == "":
        continue
    elif line.strip().startswith("["):
        crate_lines.append(line)
    elif line.startswith("move"):
        move_lines.append(line)

stacks = [[] for _ in range(N_STACKS)]
for crate_line in crate_lines[::-1]:
    for stack_idx in range(N_STACKS):
        crate = crate_line[1 + (4 * stack_idx)]
        if crate != " ":
            stacks[stack_idx].append(crate)

for move_line in move_lines:
    parsed = re.findall(r"move ([0-9]+) from ([0-9]+) to ([0-9]+)", move_line)
    assert len(parsed) == 1 and len(parsed[0]) == 3
    num_moved, from_stack, to_stack = [int(x) for x in parsed[0]]

    moved_crates = stacks[from_stack - 1][-num_moved:]
    for _ in range(num_moved):
        stacks[from_stack - 1].pop()
    stacks[to_stack - 1].extend(moved_crates)

print("".join(stack[-1] for stack in stacks))
