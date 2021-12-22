PRACTICE = False
N_DAYS = 256

with open("test.txt" if PRACTICE else "input.txt", "r") as f:
    content = f.read().strip()

state = list(map(int, content.split(",")))
fish_by_stage = [state.count(i) for i in range(9)]

def next_day(fish_by_stage):
    res = [0 for _ in range(9)]
    for i in range(1, 9):
        res[i - 1] += fish_by_stage[i]
    res[8] += fish_by_stage[0]
    res[6] += fish_by_stage[0]
    return res

for days in range(N_DAYS):
    fish_by_stage = next_day(fish_by_stage)

print(sum(fish_by_stage))
