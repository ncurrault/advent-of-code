from collections import defaultdict
from functools import reduce

PRACTICE = True
N_STEPS = 40

with open("test.txt" if PRACTICE else "input.txt", "r") as f:
    content = f.read().strip()

polymer, insertion_rules_blob = content.split("\n\n")
insertion_rules = dict(
    rule_str.split(" -> ") for rule_str in insertion_rules_blob.split("\n")
)

pair_counts = defaultdict(int)
for i in range(len(polymer) - 1):
    pair_counts[ polymer[i : i + 2] ] += 1

for step in range(N_STEPS):
    new_pair_counts = defaultdict(int)
    for pair, current_multiplicity in pair_counts.items():
        if pair in insertion_rules:
            insertion = insertion_rules[pair]
            for new_pair in (pair[0] + insertion, insertion + pair[1]):
                new_pair_counts[new_pair] += current_multiplicity
        else:
            new_pair_counts[pair] += pair_counts[pair]
    pair_counts = new_pair_counts

element_counts = defaultdict(int)
for pair, multiplicity in pair_counts.items():
    element_counts[pair[0]] += multiplicity
    element_counts[pair[1]] += multiplicity
for elem in element_counts:
    element_counts[elem] //= 2

print(max(element_counts.values()) - min(element_counts.values()))

# TOO HIGH: 3692219987039
# TODO answer here is off by one (probably due to edge cases)
