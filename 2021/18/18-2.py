from copy import deepcopy
from itertools import permutations
from math import inf

PRACTICE = False

with open("test.txt" if PRACTICE else "input.txt", "r") as f:
    content = f.read().strip()

def eval_idx(full_number, pair_indices):
    number = full_number
    for i in pair_indices:
        number = number[i]
    return number

def left_neighbor(full_number, pair_indices):
    assert pair_indices[-1] == 0 # precondition of all usages in problem
    if not any(pair_indices): # [0, 0, ... 0]
        return None
    for i in range(len(pair_indices) - 1, -1, -1):
        if pair_indices[i] == 1:
            result_idx = pair_indices[:i] + [0]
            break
    else:
        raise Exception("should be unreachable")
    result = eval_idx(full_number, result_idx)
    while not isinstance(result, int):
        result_idx.append(1)
        result = result[1]
    return result_idx

def right_neighbor(full_number, pair_indices):
    assert pair_indices[-1] == 1 # precondition of all usages in problem

    if all(pair_indices): # [1, 1, ... 1]
        return None
    for i in range(len(pair_indices) - 1, -1, -1):
        if pair_indices[i] == 0:
            result_idx = pair_indices[:i] + [1]
            break
    else:
        raise Exception("should be unreachable")
    result = eval_idx(full_number, result_idx)
    while not isinstance(result, int):
        result_idx.append(0)
        result = result[0]
    return result_idx

def try_explode(full_number, pair_indices=[]):
    number = eval_idx(full_number, pair_indices)

    if isinstance(number, int):
        return full_number, False
    else:
        left, right = number
        if len(pair_indices) >= 4 and isinstance(left, int) and isinstance(right, int):
            res = deepcopy(full_number)
            left_target_idx = left_neighbor(full_number, pair_indices + [0])
            if left_target_idx is not None:
                target_pair = eval_idx(res, left_target_idx[:-1])
                target_pair[left_target_idx[-1]] += left
            right_target_idx = right_neighbor(full_number, pair_indices + [1])
            if right_target_idx is not None:
                target_pair = eval_idx(res, right_target_idx[:-1])
                target_pair[right_target_idx[-1]] += right
            eval_idx(res, pair_indices[:-1])[pair_indices[-1]] = 0
            return res, True

        for i in range(2):
            res, was_reduced = try_explode(full_number, pair_indices=pair_indices+[i])
            if was_reduced:
                return res, True
    return full_number, False

def try_split(n):
    if isinstance(n, int):
        if n >= 10:
            return [n // 2, n // 2 + (n % 2)], True
        else:
            return n, False

    left_res, was_reduced = try_split(n[0])
    if was_reduced:
        return [left_res, n[1]], True
    right_res, was_reduced = try_split(n[1])
    if was_reduced:
        return [n[0], right_res], True

    return n, False

def reduce(n):
    while True:
        n, was_exploded = try_explode(n)
        if was_exploded:
            continue
        n, was_split = try_split(n)
        if not was_split:
            break
    return n

def magnitude(n):
    if isinstance(n, int):
        return n
    else:
        return 3 * magnitude(n[0]) + 2 * magnitude(n[1])

numbers = map(eval, content.split("\n"))
max_so_far = -inf

for left, right in permutations(numbers, 2):
    mag = magnitude(reduce([left, right]))
    if mag > max_so_far:
        max_so_far = mag

print(max_so_far)
