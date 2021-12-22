PRACTICE = False

with open("test.txt" if PRACTICE else "input.txt", "r") as f:
    content = f.read().strip()

required_close_brackets = {
    x[0]: x[1] for x in ("()", "[]", "{}", "<>")
}

scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
score = 0

for line in content.split("\n"):
    stack = []
    for i, c in enumerate(line):
        if c in required_close_brackets:
            stack.append(required_close_brackets[c])
        elif len(stack) == 0:
            break # unbalanced
        elif c == stack[-1]:
            stack.pop()
        else:
            # print(f"{line} - Expected {stack[-1]}, but found {c} instead")
            score += scores[c]
            break

print(score)
