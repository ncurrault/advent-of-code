PRACTICE = False

with open("test3.txt" if PRACTICE else "input3.txt", "r") as f:
    lines = f.read().split()

BITS = 5 if PRACTICE else 12

o2_candidates = lines
co2_candidates = lines

for i in range(BITS):
    if len(o2_candidates) > 1:
        o2_ones = 0
        o2_zeros = 0
        for line in o2_candidates:
            if line[i] == "0":
                o2_zeros += 1
            else:
                o2_ones += 1
        o2_req = "1" if o2_ones >= o2_zeros else "0"
        o2_candidates = list(filter(lambda line: line[i] == o2_req, o2_candidates))

    if len(co2_candidates) > 1:
        co2_ones = 0
        co2_zeros = 0
        for line in co2_candidates:
            if line[i] == "0":
                co2_zeros += 1
            else:
                co2_ones += 1
        co2_req = "0" if co2_ones >= co2_zeros else "1"
        co2_candidates = list(filter(lambda line: line[i] == co2_req, co2_candidates))


print("O2", o2_candidates)
print("CO2", co2_candidates)
print(eval("0b" + o2_candidates[0]) * eval("0b" + co2_candidates[0]))
