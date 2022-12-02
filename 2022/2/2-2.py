PRACTICE = False
with open("test.txt" if PRACTICE else "input.txt", "r") as f:
    file_content = f.read().strip()


def shape_points(our_play):
    return "RPS".find(our_play) + 1


def our_play(their_play, desired_outcome):
    if desired_outcome == "Y":
        return their_play

    win = (desired_outcome == "Z")
    match their_play:
        case "R":
            return "P" if win else "S"
        case "P":
            return "S" if win else "R"
        case "S":
            return "R" if win else "P"


SHAPE_LOOKUP = {
    "A": "R",
    "B": "P",
    "C": "S",
}
OUTCOME_POINTS = {
    "X": 0,
    "Y": 3,
    "Z": 6,
}


score = 0

for row in file_content.split("\n"):
    their_play_encoded, desired_outcome = row.split(" ")
    their_play = SHAPE_LOOKUP[their_play_encoded]

    score += shape_points(our_play(their_play, desired_outcome)) + OUTCOME_POINTS[desired_outcome]

print(score)
