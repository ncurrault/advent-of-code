import string
import re
import math
from collections import defaultdict

PRACTICE = False
VERBOSE = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()


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
        self.items = starting_items[:]
        self.operation_func = lambda old: eval(operation_str)
        self.divisibility_test = p_divisibility_test
        self.divisible_target = p_divisible_target
        self.non_divisible_target = p_non_divisible_target
        self.index = p_index

        self.num_inspections = 0

    def inspect_items(self):
        for i in range(len(self.items)):
            self.num_inspections += 1
            if VERBOSE:
                print(f"monkey {self.index} inspecting item with worry {self.items[i]}")
                print(
                    f"  after operation, worry is {self.operation_func(self.items[i])}"
                )
                print(
                    f"  after boredom, worry is {self.operation_func(self.items[i]) // 3}"
                )
            self.items[i] = self.operation_func(self.items[i]) // 3

    def throw_items(self):
        thrown = []
        for item in self.items:
            if item % self.divisibility_test == 0:
                target = self.divisible_target
            else:
                target = self.non_divisible_target
            if VERBOSE:
                print(f"monkey {self.index} throwing {item} to {target}")
            thrown.append((item, target))
        self.items = []
        return thrown

    def catch_item(self, item):
        self.items.append(item)

    def __str__(self):
        items_str = ", ".join(str(i) for i in self.items)
        return f"Monkey {self.index}: {items_str}"


monkeys: list[Monkey] = []
STARTING_ITEMS_STR = "Starting items: "
OPER_STR = "Operation: new = "
TEST_STR = "Test: divisible by "
TRUE_STR = "If true:"
FALSE_STR = "If false:"

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


def process_throw(item, target):
    monkeys[target].catch_item(item)


def process_throws(throws):
    for t in throws:
        process_throw(*t)


for round in range(20):
    for monkey in monkeys:
        monkey.inspect_items()
        process_throws(monkey.throw_items())


inspections = [monkey.num_inspections for monkey in monkeys]
inspections.sort()
print(inspections[-1] * inspections[-2])
