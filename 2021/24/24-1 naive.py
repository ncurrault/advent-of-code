from itertools import product

with open("input.txt", "r") as f:
    content = f.read().strip()

DIGITS = "987654321"
for model_number in product(DIGITS, repeat=14):
    pending_input = model_number
    w, x, y, z = 0, 0, 0, 0
    for line in content.split("\n"):
        op, *args = line.split(" ")
        match op:
            case "inp":
                assert len(pending_input) > 0
                assert len(args) == 1
                var_to_set, = args
                input_val = pending_input[0]
                pending_input = pending_input[1:]
                exec(f"{var_to_set} = {input_val}")
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
    print("".join(model_number), end="\r")
    if not z:
        print("\n")
        print("".join(model_number))
        break
