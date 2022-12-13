import string
import re
import math
from collections import defaultdict
from enum import Enum

PRACTICE = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()


class ComparisonResult(Enum):
    LESS_THAN = -1
    EQUAL_TO = 0
    GREATER_THAN = 1


def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return ComparisonResult.LESS_THAN
        if left > right:
            return ComparisonResult.GREATER_THAN
        else:
            return ComparisonResult.EQUAL_TO
    if isinstance(left, list) and isinstance(right, list):
        for i in range(min(len(left), len(right))):
            item_compare = compare(left[i], right[i])
            if item_compare != ComparisonResult.EQUAL_TO:
                return item_compare

        if len(left) < len(right):
            return ComparisonResult.LESS_THAN
        elif len(left) > len(right):
            return ComparisonResult.GREATER_THAN
        else:
            return ComparisonResult.EQUAL_TO

    if isinstance(left, int):
        return compare([left], right)
    if isinstance(right, int):
        return compare(left, [right])

    raise ValueError(f"could not compare {left} and {right}")


# quicksort with custom comparison
def sort_packets(packets):
    if len(packets) < 2:
        return packets
    pivot = packets[0]
    left = []
    right = []
    for packet in packets[1:]:
        cmp = compare(packet, pivot)
        if cmp == ComparisonResult.LESS_THAN:
            left.append(packet)
        else:
            right.append(packet)
    return sort_packets(left) + [pivot] + sort_packets(right)


packets = [eval(p) for p in file_content.split()]
divider_packets = [[[2]], [[6]]]
sorted_packets = sort_packets(packets + divider_packets)

res = 1
for p in divider_packets:
    res *= sorted_packets.index(p) + 1
print(res)
