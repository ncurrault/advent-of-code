with open("input3.txt", "r") as f:
    lines = f.read().split()

BITS = 12

ones = [0] * BITS
zeros = [0] * BITS
for line in lines:
    for i in range(BITS):
        if line[i] == "1":
            ones[i] += 1
        else:
            zeros[i] += 1

gamma = "0b"
epsilon = "0b"
for i in range(BITS):
    if ones[i] > zeros[i]:
        gamma += "1"
        epsilon += "0"
    elif ones[i] < zeros[i]:
        gamma += "0"
        epsilon += "1"
    else:
        raise Exception("undefined")

print(eval(gamma) * eval(epsilon))
