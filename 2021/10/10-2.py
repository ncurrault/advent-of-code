PRACTICE = False

with open("test.txt" if PRACTICE else "input.txt", "r") as f:
    content = f.read().strip()

required_close_brackets = {
    x[0]: x[1] for x in ("()", "[]", "{}", "<>")
}

score_key = {")": 1, "]": 2, "}": 3, ">": 4}
scores = []

for line in content.split("\n"):
    stack = []
    for i, c in enumerate(line):
        if c in required_close_brackets:
            stack.append(required_close_brackets[c])
        elif len(stack) == 0:
            raise Exception("this should never happen")
        elif c == stack[-1]:
            stack.pop()
        else:
            break
    else:
        line_score = 0
        for c in stack[::-1]:
            line_score *= 5
            line_score += score_key[c]
        scores.append(line_score)

scores.sort()
while len(scores) > 1:
    scores.pop()
    scores.pop(0)
print(scores[0])
