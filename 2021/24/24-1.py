with open("input.txt", "r") as f:
    content = f.read().strip()

lines = content.split("\n")

DIGITS = "123456789"

init_state = (0, 0, 0, 0, 0)
to_explore = [init_state]
visited = set()
traceback = {}

while len(to_explore) > 0:
    state = to_explore.pop(0)
    if state in visited:
        continue
    visited.add(state)
    instruction_ptr, w, x, y, z = state

    while instruction_ptr < len(lines):
        op, *args = lines[instruction_ptr].split(" ")
        match op:
            case "inp":
                var_to_set, = args
                for d in DIGITS:
                    exec(f"{var_to_set} = {d}")
                    new_state = (instruction_ptr + 1, w, x, y, z)
                    to_explore.append(new_state)
                    traceback[new_state] = (state, d)
                break
            case "add":
                assert len(args) == 2
                term1, term2 = args
                exec(f"{term1} += {term2}")
            case "mul":
                assert len(args) == 2
                term1, term2 = args
                exec(f"{term1} *= {term2}")
            case "div":
                assert len(args) == 2
                term1, term2 = args
                exec(f"{term1} //= {term2}")
            case "mod":
                assert len(args) == 2
                term1, term2 = args
                exec(f"{term1} %= {term2}")
            case "eql":
                assert len(args) == 2
                term1, term2 = args
                exec(f"{term1} = int({term1} == {term2})")
        instruction_ptr += 1
    else:
        if z != 0:
            continue

        state_trace = state
        model_num_rev = []
        while state_trace != init_state:
            state_trace, d = traceback[state_trace]
            model_num_rev.append(d)
        print("".join(model_num_rev[::-1]))
