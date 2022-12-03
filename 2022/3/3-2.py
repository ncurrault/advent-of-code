import string

PRACTICE = False
with open("test.txt" if PRACTICE else "input.txt", "r") as f:
    file_content = f.read().strip()

alphabets = string.ascii_lowercase + string.ascii_uppercase
PRIORITY = {c: alphabets.find(c) + 1 for c in alphabets}

res = 0

lines = file_content.split()

for group_start in range(0, len(lines), 3):
    group = lines[group_start : group_start + 3]
    common_elements = set(alphabets)
    for g in group:
        common_elements.intersection_update(g)
    assert len(common_elements) == 1
    res += PRIORITY[common_elements.pop()]

print(res)
