from collections import defaultdict
from math import inf

PRACTICE = False

key = [
    "abcefg",  # 0
    "cf",      # 1*
    "acdeg",   # 2
    "acdfg",   # 3
    "bcdf",    # 4*
    "abdfg",   # 5
    "abdefg",  # 6
    "acf",     # 7*
    "abcdefg", # 8*
    "abcdfg",  # 9
]
def apply_permutation(permutation, digit):
    res = ""
    for segment in digit:
        res += "abcdefg"[permutation.find(segment)]
    return "".join(sorted(res))

with open("test.txt" if PRACTICE else "input.txt", "r") as f:
    content = f.read().strip()

res = 0

for line in content.split("\n"):
    training_str, code_str = line.split(" | ")

    training_digits = training_str.split()
    known_mappings = {}
    for d in training_digits:
        for easy_digit in (1, 4, 7, 8):
            if len(d) == len(key[easy_digit]):
                known_mappings[easy_digit] = d

    # a is known ("7" - "1")
    # c/f (2 options from 1)
    # b/d (2 options from "4" - "1")

    possible_cf = known_mappings[1]
    known_a = (set(known_mappings[7]) - set(possible_cf)).pop()
    possible_bd = "".join(set(known_mappings[4]) - set(possible_cf))
    possible_eg = "".join(
        set("abcdefg") - set(possible_cf) - set(possible_bd) - {known_a}
    )

    for encoded_permutation in range(8):
        cf = possible_cf[::1 if encoded_permutation & 1 else -1]
        bd = possible_bd[::1 if encoded_permutation & 2 else -1]
        eg = possible_eg[::1 if encoded_permutation & 4 else -1]
        permutation = known_a + bd[0] + cf[0] + bd[1] + eg[0] + cf[1] + eg[1]
        assert set(permutation) == set("abcdefg")
        for d in training_digits:
            if apply_permutation(permutation, d) not in key:
                break
        else:
            break
    else:
        raise Exception("your code is bad and you should feel bad")

    code = code_str.split()
    code_translated = ""
    for digit in code:
        proper_digit = apply_permutation(permutation, digit)
        code_translated += str(key.index(proper_digit))
    while code_translated.startswith("0"):
        code_translated = code_translated[1:]
    res += eval(code_translated)

print(res)
