PRACTICE = False

with open("test.txt" if PRACTICE else "input.txt", "r") as f:
    lines = f.read().split()

depths = [int(l) for l in lines]
print([depths[i + 1] > depths[i] for i in range(len(depths) - 1)].count(True))
