from collections import defaultdict
from functools import reduce

PRACTICE = False
N_STEPS = 10

with open("test.txt" if PRACTICE else "input.txt", "r") as f:
    content = f.read().strip()

polymer, insertion_rules_blob = content.split("\n\n")
insertion_rules = dict(
    rule_str.split(" -> ") for rule_str in insertion_rules_blob.split("\n")
)

for step in range(N_STEPS):
    new_polymer = ""
    for i in range(len(polymer) - 1):
        new_polymer += polymer[i]
        new_polymer += insertion_rules.get(polymer[i : i + 2], "")
    new_polymer += polymer[-1]
    polymer = new_polymer
    # print(f"After step {step}:", polymer)

element_counts = defaultdict(int)
for c in polymer:
    element_counts[c] += 1
print(max(element_counts.values()) - min(element_counts.values()))
