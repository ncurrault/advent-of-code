from itertools import product
from tqdm import tqdm
from functools import cache

PRACTICE = False

p1_pos = 4 if PRACTICE else 7
p2_pos = 8 if PRACTICE else 5

next_roll = 1
num_rolls = 0
def roll():
    global next_roll
    global num_rolls
    res = next_roll
    next_roll += 1
    if next_roll == 101:
        next_roll = 1
    num_rolls += 1
    return res


p1_score = 0
p2_score = 0

while max(p1_score, p2_score) < 1000:
    p1move = roll() + roll() + roll()
    p1_pos = (p1_pos + p1move) % 10
    if p1_pos == 0:
        p1_pos = 10
    p1_score += p1_pos
    if p1_score >= 1000:
        break

    p2move = roll() + roll() + roll()
    p2_pos = (p2_pos + p2move) % 10
    if p2_pos == 0:
        p2_pos = 10
    p2_score += p2_pos

print(num_rolls * min(p1_score, p2_score))
