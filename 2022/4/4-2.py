PRACTICE = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()


res = 0

for line in file_content.split():
    first_elf, second_elf = line.split(",")
    a, b = [int(x) for x in first_elf.split("-")]
    c, d = [int(x) for x in second_elf.split("-")]

    if (
        (a <= c and c <= b)
        or (a <= d and d <= b)
        or (c <= a and a <= d)
        or (c <= b and b <= d)
    ):
        res += 1

print(res)
