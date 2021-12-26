with open("input.txt", "r") as f:
    content = f.read().strip()

model_number = list("13579246899999")

pending_input = model_number[:]
w, x, y, z = 0, 0, 0, 0
for line in content.split("\n"):
    op, *args = line.split(" ")
    match op:
        case "inp":
            assert len(pending_input) > 0
            assert len(args) == 1
            var_to_set, = args
            input_val = pending_input.pop(0)
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

print(z)
