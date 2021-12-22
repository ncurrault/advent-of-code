from itertools import product
from dataclasses import dataclass
from collections import defaultdict

PRACTICE = False


@dataclass(frozen=True)
class GameState:
    p1_pos: int
    p2_pos: int
    p1_score: int
    p2_score: int
    p1_turn: bool


num_universes = {
    GameState(
        p1_pos=4 if PRACTICE else 7,
        p2_pos=8 if PRACTICE else 5,
        p1_score=0,
        p2_score=0,
        p1_turn=True,
    ): 1
}

p1_victories = 0
p2_victories = 0

distribution = defaultdict(int)
for rolls in product(range(1, 4), repeat=3):
    distribution[sum(rolls)] += 1
distribution = dict(distribution)

while len(num_universes) > 0:
    new_universes = defaultdict(int)
    for old_state, n_univ in num_universes.items():
        if old_state.p1_score >= 21:
            p1_victories += n_univ
            continue
        if old_state.p2_score >= 21:
            p2_victories += n_univ
            continue
        for roll_sum, multiplicity in distribution.items():
            p1_pos = old_state.p1_pos
            p2_pos = old_state.p2_pos
            p1_score = old_state.p1_score
            p2_score = old_state.p2_score
            if old_state.p1_turn:
                p1_pos = (p1_pos + roll_sum) % 10
                if p1_pos == 0:
                    p1_pos = 10
                p1_score += p1_pos
            else:
                p2_pos = (p2_pos + roll_sum) % 10
                if p2_pos == 0:
                    p2_pos = 10
                p2_score += p2_pos

            new_state = GameState(p1_pos=p1_pos, p2_pos=p2_pos,
                p1_score=p1_score, p2_score=p2_score,
                p1_turn=(not old_state.p1_turn),
            )
            new_universes[new_state] += n_univ * multiplicity

    num_universes = dict(new_universes)

print(p1_victories)
print(p2_victories)
