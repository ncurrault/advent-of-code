PRACTICE = False
with open("test.txt" if PRACTICE else "input.txt", "r") as f:
    file_content = f.read().strip()


def shape_points(our_play):
    return "RPS".find(our_play) + 1


def outcome_points(their_play, our_play):
    if their_play == our_play:
        return 3

    pair = "".join(sorted(their_play + our_play))
    match pair:
        case "PR":
            win = (our_play == "P")
        case "RS":
            win = (our_play == "R")
        case "PS":
            win = (our_play == "S")
        case _:
            raise ValueError(pair)
    return 6 if win else 0


SHAPE_LOOKUP = {
    "A": "R",
    "B": "P",
    "C": "S",
    "X": "R",
    "Y": "P",
    "Z": "S",
}

score = 0

for row in file_content.split("\n"):
    their_play_encoded, our_play_encoded = row.split(" ")

    their_play = SHAPE_LOOKUP[their_play_encoded]
    our_play = SHAPE_LOOKUP[our_play_encoded]
    
    score += shape_points(our_play) + outcome_points(their_play, our_play)

print(score)