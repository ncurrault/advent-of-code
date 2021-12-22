from collections import defaultdict

PRACTICE = False

with open("test.txt" if PRACTICE else "input.txt", "r") as f:
    content = f.read().strip()

adjacency_map = defaultdict(list)

for line in content.split("\n"):
    a, b = line.split("-")
    adjacency_map[a].append(b)
    adjacency_map[b].append(a)

unfinished_paths = [(["start"], False)]
num_paths = 0

while len(unfinished_paths) > 0:
    path, double_visit_used = unfinished_paths.pop(0)
    if path[-1] == "end":
        num_paths += 1
        continue
    for next_step in adjacency_map[path[-1]]:
        if next_step in path and not next_step.isupper():  # big cave
            if next_step != "start" and not double_visit_used:
                unfinished_paths.append((path + [next_step], True))
            continue
        unfinished_paths.append((path + [next_step], double_visit_used))

print(num_paths)
