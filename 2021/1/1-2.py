PRACTICE = False

with open("test.txt" if PRACTICE else "input.txt", "r") as f:
    lines = f.read().split()

depths_raw = [int(l) for l in lines]
depths = [depths_raw[i] + depths_raw[i+1] + depths_raw[i+2] for i in range(len(depths_raw) - 2)]

print([depths[i + 1] > depths[i] for i in range(len(depths) - 1)].count(True))
