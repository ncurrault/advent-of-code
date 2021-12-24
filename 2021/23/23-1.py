from itertools import count
from collections import defaultdict
from math import inf
from heapq import heappush, heappop

PRACTICE = False

"""
current state is represented as a string "abcdefghijklmno" (len 15) where
#############
#ab.e.h.k.no#
###c#f#i#l###
  #d#g#j#m#
  #########
or
#############
#01.4.7.0.34#
###2#5#8#1###
  #3#6#9#2#
 #########
"""

start_state = "..BA.CD.BC.DA.." if PRACTICE else "..CC.AA.BD.DB.."
end_state = "..AA.BB.CC.DD.."


def is_hallway(loc):
    assert loc >= 0 and loc <= 14
    return loc in (0, 1, 4, 7, 10, 13, 14)


def is_occupied(state, loc):
    return state[loc] in "ABCD"

LEFT_PATHS = {
    2: [1, 0],
    5: [4, None, 1, 0],
    8: [7, None, 4, None, 1, 0],
    11: [10, None, 7, None, 4, None, 1, 0],
}
RIGHT_PATHS = {
    2: [4, None, 7, None, 10, None, 13, 14],
    5: [7, None, 10, None, 13, 14],
    8: [10, None, 13, 14],
    11: [13, 14],
}
PER_MOVE_ENERGIES = {"A": 1, "B": 10, "C": 100, "D": 1000}
ROOMS = [(3, 2), (6, 5), (9, 8), (12, 11)]
ROOM_BOTTOMS = [x[0] for x in ROOMS]

print_state_str_format = """
#############
#{0}{1}.{4}.{7}.{10}.{13}{14}#
###{2}#{5}#{8}#{11}###
  #{3}#{6}#{9}#{12}#
  #########
"""
def state_str(state):
    return print_state_str_format.format(*state)
def print_state(state):
    print(state_str(state))

def swap_chars(s, i, j):
    l = list(s)
    l[i], l[j] = l[j], l[i]
    return "".join(l)

def room_destinations_from_hallway(state, traveler):
    for bottom, top in ROOMS:
        if is_occupied(state, top):
            continue
        elif is_occupied(state, bottom) and state[bottom] != traveler:
            continue
        yield top if is_occupied(state, bottom) else bottom

def hallway_to_room_dist(state, hallway_loc, destination):
    plus_one = destination in ROOM_BOTTOMS
    if plus_one:
        destination -= 1
    # TODO just subset of [1,4,7,10,13] in open interval?
    blockers = {
        (0, 2): [1],
        (0, 5): [1, 4],
        (0, 8): [1, 4, 7],
        (0, 11): [1, 4, 7, 10],
        (1, 5): [4],
        (1, 8): [4, 7],
        (1, 11): [4, 7, 10],
        (4, 8): [7],
        (4, 11): [10],
        (7, 2): [4],
        (7, 11): [10],
        (10, 2): [4, 7],
        (10, 5): [7],
        (13, 2): [4, 7, 10],
        (13, 5): [7, 10],
        (13, 8): [10],
        (14, 2): [4, 7, 10, 13],
        (14, 5): [7, 10, 13],
        (14, 8): [10, 13],
        (14, 11): [13],
    }.get((hallway_loc, destination), [])
    for b in blockers:
        if is_occupied(state, b):
            return
    return {
        (0, 2): 3,
        (0, 5): 5,
        (0, 8): 7,
        (0, 11): 9,
        (1, 5): 4,
        (1, 8): 6,
        (1, 11): 8,
        (4, 8): 4,
        (4, 11): 6,
        (7, 2): 4,
        (7, 11): 4,
        (10, 2): 6,
        (10, 5): 4,
        (13, 2): 8,
        (13, 5): 6,
        (13, 8): 4,
        (14, 2): 9,
        (14, 5): 7,
        (14, 8): 5,
        (14, 11): 3
    }.get((hallway_loc, destination), 2) + int(plus_one)

def valid_transitions(state):
    for loc in range(15):
        if not is_occupied(state, loc):
            continue
        occupant = state[loc]
        per_move_energy = PER_MOVE_ENERGIES[occupant]
        if is_hallway(loc):
            for destination in room_destinations_from_hallway(state, occupant):
                d = hallway_to_room_dist(state, loc, destination)
                if d is None:
                    continue
                yield swap_chars(state, loc, destination), d * per_move_energy
        else:
            bottoms = [room[0] for room in ROOMS]
            current_loc = loc
            if loc in bottoms:
                if is_occupied(state, loc - 1):
                    continue # blocked in
                else:
                    current_loc -= 1
            # can now assume we're at the top of a room: 2-5-8-11
            for path in (LEFT_PATHS[current_loc], RIGHT_PATHS[current_loc]):
                distance = int(loc in bottoms) + 1
                for destination in path:
                    distance += 1
                    if destination is None:
                        continue
                    if is_occupied(state, destination):
                        break
                    yield swap_chars(state, loc, destination), distance * per_move_energy

# source for pq implementation:
# https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes
pq = []                         # list of entries arranged in a heap
entry_finder = {}               # mapping of tasks to entries
REMOVED = '<removed-task>'      # placeholder for a removed task
counter = count()               # unique sequence count

def add_task(task, priority=0):
    'Add a new task or update the priority of an existing task'
    if task in entry_finder:
        remove_task(task)
    count = next(counter)
    entry = [priority, count, task]
    entry_finder[task] = entry
    heappush(pq, entry)

def remove_task(task):
    'Mark an existing task as REMOVED.  Raise KeyError if not found.'
    entry = entry_finder.pop(task)
    entry[-1] = REMOVED

def pop_task():
    'Remove and return the lowest priority task. Raise KeyError if empty.'
    while pq:
        priority, count, task = heappop(pq)
        if task is not REMOVED:
            del entry_finder[task]
            return task
    raise KeyError('pop from an empty priority queue')

distance = defaultdict(lambda: inf)
distance[start_state] = 0
add_task(start_state)

while distance[end_state] == inf:
    state = pop_task()

    for next_state, energy in valid_transitions(state):
        candidate_distance = distance[state] + energy
        if candidate_distance < distance[next_state]:
            distance[next_state] = candidate_distance
            add_task(next_state, candidate_distance)

print(distance[end_state])
