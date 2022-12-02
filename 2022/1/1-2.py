with open("input.txt", "r") as f:
    content = f.read()

elf_list_strs = content.split("\n\n")
elf_lists = [
    [int(food) for food in elf_list_str.strip().split("\n")]
    for elf_list_str in elf_list_strs
]

amounts = [sum(l) for l in elf_lists]
print(sum(sorted(amounts)[-3:]))
