import string

PRACTICE = False
with open("test.txt" if PRACTICE else "input.txt", "r") as f:
    file_content = f.read().strip()

alphabets = string.ascii_lowercase + string.ascii_uppercase
PRIORITY = {c: alphabets.find(c) + 1 for c in alphabets}

res = 0

for line in file_content.split():
    assert len(line) % 2 == 0
    compartment_a = line[: len(line) // 2]
    compartment_b = line[len(line) // 2 :]
    mistakes = set(compartment_a).intersection(set(compartment_b))
    assert len(mistakes) == 1
    res += PRIORITY[mistakes.pop()]

print(res)
