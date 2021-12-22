from collections import defaultdict
from functools import cache
from math import inf

PRACTICE = False

target_x_min = 20 if PRACTICE else 235
target_x_max = 30 if PRACTICE else 259
target_y_min = -10 if PRACTICE else -118
target_y_max = -5 if PRACTICE else -62

def path_steps(vx, vy):
    x, y = 0, 0
    while True:
        yield x, y, vx, vy
        x += vx
        y += vy
        if vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1
        vy -= 1

def hits_target(vx, vy):
    path_gen = path_steps(vx, vy)
    for x, y, vx, vy in path_gen:
        if x >= target_x_min and x <= target_x_max and y >= target_y_min and y <= target_y_max:
            return True
        if vx == 0:
            break # probe will remain in this vertical line
    if x < target_x_min or x > target_x_max:
        return False
    while y >= target_y_min or vy > 0:
        if y >= target_y_min and y <= target_y_max:
            return True
        y += vy
        vy -= 1
    return False

def max_height(vy):
    return vy * (vy + 1) // 2

# max y depends only on vy
# so for each vy, we want to know if a vx exists s.t. it makes it into the area
# only have to try from 1 through target_x_max
max_so_far = -inf

vy = 1
while True:
    for vx in range(1, target_x_max + 1):
        if hits_target(vx, vy):
            print( max_height(vy) )
            break
    vy += 1

# TODO principled stopping condition
