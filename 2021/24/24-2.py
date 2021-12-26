from functools import lru_cache

with open("input.txt", "r") as f:
    content = f.read().strip()

lines = content.split("\n")

DIGITS = "123456789"

init_state = (0, 0, 0, 0, 0)

@lru_cache(maxsize=10**7)
def explore(state):
    instruction_ptr, w, x, y, z = state

    while instruction_ptr < len(lines):
        op, *args = lines[instruction_ptr].split(" ")
        match op:
            case "inp":
                var_to_set, = args
                for d in DIGITS:
                    rhs = int(d)
                    match var_to_set:
                        case "w":
                            new_state = (instruction_ptr + 1, rhs, x, y, z)
                        case "x":
                            new_state = (instruction_ptr + 1, w, rhs, y, z)
                        case "y":
                            new_state = (instruction_ptr + 1, w, x, rhs, z)
                        case "z":
                            new_state = (instruction_ptr + 1, w, x, y, rhs)
                        case _:
                            raise Exception
                    res = explore(new_state)
                    if res is not None:
                        return str(d) + res
                return
            case "add":
                assert len(args) == 2
                var_to_set, term2 = args
                rhs = eval(f"{var_to_set} + {term2}")
            case "mul":
                assert len(args) == 2
                var_to_set, term2 = args
                rhs = eval(f"{var_to_set} * {term2}")
            case "div":
                assert len(args) == 2
                var_to_set, term2 = args
                rhs = eval(f"{var_to_set} // {term2}")
            case "mod":
                assert len(args) == 2
                var_to_set, term2 = args
                rhs = eval(f"{var_to_set} % {term2}")
            case "eql":
                assert len(args) == 2
                var_to_set, term2 = args
                rhs = eval(f"int({var_to_set} == {term2})")
        match var_to_set:
            case "w":
                w = rhs
            case "x":
                x = rhs
            case "y":
                y = rhs
            case "z":
                z = rhs
            case _:
                raise Exception
        instruction_ptr += 1
    if z == 0:
        return ""

print(explore(init_state))
