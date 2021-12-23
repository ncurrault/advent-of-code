from itertools import count
from enum import Enum

PRACTICE = True

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
    2: [1, 0]
    5: [4, None, 1, 0]
    8: [7, None, 4, None, 1, 0]
    11: [10, None, 7, None, 4, None, 1, 0]
}
RIGHT_PATHS = {
    2: [4, None, 7, None, 10, None, 13, 14]
    5: [7, None, 10, None, 13, 14]
    8: [10, None, 13, 14]
    11: [13, 14]
}
PER_MOVE_ENERGIES = {"A": 1, "B": 10, "C": 100, "D": 1000}
ROOMS = [(3, 2), (6, 5), (9, 8), (12, 11)]

def swap_chars(s, i, j):
    l = list(s)
    l[i], l[j] = l[j], l[i]
    return "".join(l)

def room_destinations_from_hallway(state, traveler):
    for bottom, top in rooms:
        if is_occupied(state, top):
            continue
        elif is_occupied(state, bottom) and state[bottom] != traveler:
            continue
        yield top if is_occupied(state, bottom) else bottom

def valid_transitions(state):
    for loc in range(15):
        if not is_occupied(state, loc):
            continue
        occupant = state[loc]
        per_move_energy = PER_MOVE_ENERGIES[occupant]
        if is_hallway(loc):
            pass  # must move into a room
        else:
            bottoms = [room[0] for room in ROOMS]
            current_loc = loc
            if loc in bottoms:
                if is_occupied(statte, loc - 1):
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
