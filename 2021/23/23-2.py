from itertools import count
from collections import defaultdict
from math import inf
from heapq import heappush, heappop

PRACTICE = False

"""
current state is represented as a length-23 string

#######################
#         1   1    2 2#
#01 . 6 . 1 . 6 .  1 2#
### 2 # 7 #12 #17 #####
  # 3 # 8 #13 #18 #
  # 4 # 9 #14 #19 #
  # 5 #10 #15 #20 #
  #################
"""

start_state = "..BDDA.CCBD.BBAC.DACA.." if PRACTICE else "..CDDC.ACBA.BBAD.DACB.."
end_state = "..AAAA.BBBB.CCCC.DDDD.."

NUM_SPACES = 23
assert len(start_state) == NUM_SPACES
assert len(end_state) == NUM_SPACES

CENTER_HALLWAY = [1, 6, 11, 16, 21]
FULL_HALLWAY = [0] + CENTER_HALLWAY + [22]

# TODO could have generated these from the hallway, just need "insertion points"
LEFT_PATHS = {
    2: [1, 0],
    7: [6, None, 1, 0],
    12: [11, None, 6, None, 1, 0],
    17: [16, None, 11, None, 6, None, 1, 0],
}
RIGHT_PATHS = {
    2: [6, None, 11, None, 16, None, 21, 22],
    7: [11, None, 16, None, 21, 22],
    12: [16, None, 21, 22],
    17: [21, 22],
}
PER_MOVE_ENERGIES = {"A": 1, "B": 10, "C": 100, "D": 1000}
ROOMS = [(5, 4, 3, 2), (10, 9, 8, 7), (15, 14, 13, 12), (20, 19, 18, 17)]
ROOM_TOPS = [x[-1] for x in ROOMS]

def is_hallway(loc):
    return loc in FULL_HALLWAY

def is_occupied(state, loc):
    return state[loc] in "ABCD"

def swap_chars(s, i, j):
    l = list(s)
    l[i], l[j] = l[j], l[i]
    return "".join(l)

def room_destinations_from_hallway(state, traveler):
    for room in ROOMS:
        *bottom, top = room
        if is_occupied(state, top):
            continue
        for b in bottom:
            if is_occupied(state, b) and state[b] != traveler:
                break
        else:
            for x in room:
                if not is_occupied(state, x):
                    yield x
                    break

def to_room_top(state, loc):
    for room in ROOMS:
        if loc in room:
            steps_within_room = room[::-1].index(loc)
            return room[-1], steps_within_room
    raise Exception

def hallway_to_room_dist(state, hallway_loc, destination):
    destination, steps_within_room = to_room_top(state, destination)

    for b in CENTER_HALLWAY:
        if b <= min(hallway_loc, destination) or b >= max(hallway_loc, destination):
            continue
        if is_occupied(state, b):
            return

    return {
        (0, 2): 3,
        (0, 7): 5,
        (0, 12): 7,
        (0, 17): 9,
        (1, 7): 4,
        (1, 12): 6,
        (1, 17): 8,
        (6, 12): 4,
        (6, 17): 6,
        (11, 2): 4,
        (11, 17): 4,
        (16, 2): 6,
        (16, 7): 4,
        (21, 2): 8,
        (21, 7): 6,
        (21, 12): 4,
        (22, 2): 9,
        (22, 7): 7,
        (22, 12): 5,
        (22, 17): 3
    }.get((hallway_loc, destination), 2) + steps_within_room

def valid_transitions(state, goal_state):
    for loc in range(NUM_SPACES):
        if not is_occupied(state, loc):
            continue
        occupant = state[loc]
        per_move_energy = PER_MOVE_ENERGIES[occupant]
        if is_hallway(loc):
            for destination in room_destinations_from_hallway(state, occupant):
                d = hallway_to_room_dist(state, loc, destination)
                if d is None:
                    continue
                if goal_state[destination] != occupant:
                    continue
                yield swap_chars(state, loc, destination), d * per_move_energy
        else:
            current_loc, steps_within_room = to_room_top(state, loc)
            # check if blocked in
            if any(is_occupied(state, potential_blocker) for potential_blocker in range(current_loc, loc)):
                continue
            # can now assume we're at the top of a room: 2-7-12-17
            for path in (LEFT_PATHS[current_loc], RIGHT_PATHS[current_loc]):
                distance = steps_within_room + 1
                for destination in path:
                    distance += 1
                    if destination is None:
                        continue
                    if is_occupied(state, destination):
                        break
                    yield swap_chars(state, loc, destination), distance * per_move_energy

print_state_str_format = """
#############
#{0}{1}.{6}.{11}.{16}.{21}{22}#
###{2}#{7}#{12}#{17}###
  #{3}#{8}#{13}#{18}#
  #{4}#{9}#{14}#{19}#
  #{5}#{10}#{15}#{20}#
  #########
"""

def state_str(state):
    return print_state_str_format.format(*state)
def print_state(state):
    print(state_str(state))

map_template = """
#############
#ab.g.l.q.vw#
###c#h#m#r###
  #d#i#n#s#
  #e#j#o#t#
  #f#k#p#u#
  #########
""".strip()

def parse_map(state_map):
    state_map = state_map.strip()
    res = ""
    for idx in (map_template.index(c) for c in "abcdefghijklmnopqrstuvw"):
        res += state_map[idx]

    assert state_str(res).strip() == state_map.strip()
    return res

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

while True:
    state = pop_task()
    if state == end_state:
        break

    for next_state, energy in valid_transitions(state, end_state):
        candidate_distance = distance[state] + energy
        if candidate_distance < distance[next_state]:
            distance[next_state] = candidate_distance
            add_task(next_state, candidate_distance)

print(distance[end_state])
