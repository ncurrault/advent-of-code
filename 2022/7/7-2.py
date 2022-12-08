from collections import defaultdict

PRACTICE = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()

lines = file_content.split("\n")
directory_sizes: defaultdict[tuple[str], int] = defaultdict(int)
dirs_listed: set[tuple[str]] = set()

pwd = ()
parsing_ls = False

for line in lines:
    line_split = line.split()
    if line_split[0] == "$":
        command = line_split[1]
        if command == "cd":
            parsing_ls = False
            arg = line_split[2]
            if arg == "/":
                pwd = ()
            elif arg == "..":
                pwd = pwd[:-1]
            else:
                pwd = pwd + (arg,)
        elif command == "ls":
            parsing_ls = pwd not in dirs_listed
            dirs_listed.add(pwd)
        else:
            raise ValueError(f"unrecognized command: {command}")
    elif parsing_ls:
        if line_split[0].isdigit():
            file_size = int(line_split[0])
            for i in range(len(pwd) + 1):
                directory_sizes[pwd[:i]] += file_size

TOTAL_SPACE = 70000000
SPACE_REQUIRED = 30000000
space_used = directory_sizes[()]

space_required = SPACE_REQUIRED - TOTAL_SPACE + space_used

print(min(size for size in directory_sizes.values() if size >= space_required))
