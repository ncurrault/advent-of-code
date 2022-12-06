import re
import string

PRACTICE = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()


last_four = ""

for i in range(4, len(file_content) + 1):
    last_four = file_content[i - 4 : i]
    if len(set(last_four)) == 4:
        print(i)
        break
