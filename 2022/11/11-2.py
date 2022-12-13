import string
import re
import math
from tqdm import tqdm
from collections import defaultdict

PRACTICE = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()


class Item:
    def __init__(self, value):
        self.values = [value % div for div in relevant_divisors]

    def apply_func(self, f):
        self.values = [
            f(value) % div for value, div in zip(self.values, relevant_divisors)
        ]

    def is_divisible(self, div):
        assert div in relevant_divisors
        return self.values[relevant_divisors.index(div)] == 0


class Monkey:
    def __init__(
        self,
        starting_items,
        operation_str,
        p_divisibility_test,
        p_divisible_target,
        p_non_divisible_target,
        p_index,
    ):
        self.items = [Item(x) for x in starting_items]
        self.operation_func = lambda old: eval(operation_str)
        self.divisibility_test = p_divisibility_test
        self.divisible_target = p_divisible_target
        self.non_divisible_target = p_non_divisible_target
        self.index = p_index

        self.num_inspections = 0

    def turn(self):
        thrown = defaultdict(list)
        for item in self.items:
            self.num_inspections += 1
            item.apply_func(self.operation_func)
            if item.is_divisible(self.divisibility_test):
                target = self.divisible_target
            else:
                target = self.non_divisible_target
            thrown[target].append(item)
        self.items.clear()
        return dict(thrown)

    def catch_items(self, items):
        self.items.extend(items)


monkeys: list[Monkey] = []
STARTING_ITEMS_STR = "Starting items: "
OPER_STR = "Operation: new = "
TEST_STR = "Test: divisible by "
TRUE_STR = "If true:"
FALSE_STR = "If false:"

relevant_divisors = []
for line in file_content.split("\n"):
    if line.strip().startswith(TEST_STR):
        relevant_divisors.append(int(line.split()[-1]))

for monkey_text in file_content.split("\n\n"):
    for line in monkey_text.split("\n"):
        line = line.strip()
        if line.startswith("Monkey"):
            current_monkey_idx = int(line.split()[-1][:-1])
        if line.startswith(STARTING_ITEMS_STR):
            items = [int(item) for item in line[len(STARTING_ITEMS_STR) :].split(", ")]
        elif line.startswith(OPER_STR):
            operation = line[len(OPER_STR) :]
        elif line.startswith(TEST_STR):
            test_div_by = int(line.split()[-1])
        elif line.startswith(TRUE_STR):
            div_target = int(line.split()[-1])
        elif line.startswith(FALSE_STR):
            nondiv_target = int(line.split()[-1])
            assert len(monkeys) == current_monkey_idx
            monkeys.append(
                Monkey(
                    items,
                    operation,
                    test_div_by,
                    div_target,
                    nondiv_target,
                    current_monkey_idx,
                )
            )


def process_throws(throws):
    for target, items in throws.items():
        monkeys[target].catch_items(items)


N_ROUNDS = 10000
prog = tqdm(total=N_ROUNDS * len(monkeys))

for round in range(N_ROUNDS):
    for monkey in monkeys:
        process_throws(monkey.turn())
        prog.update()

prog.close()


inspections = [monkey.num_inspections for monkey in monkeys]
inspections.sort()
print(inspections[-1] * inspections[-2])
