PRACTICE = False
N_DAYS = 80

with open("test.txt" if PRACTICE else "input.txt", "r") as f:
    content = f.read().strip()

state = list(map(int, content.split(",")))

def next_day(state):
    new_state = []
    num_new = 0
    for fish in state:
        if fish == 0:
            new_state.append(6)
            num_new += 1
        else:
            new_state.append(fish - 1)

    return new_state + [8] * num_new

for days in range(N_DAYS):
    state = next_day(state)
    # print("After {:2} days: ".format(days + 1) + ",".join(map(str, state)))

print(len(state))
