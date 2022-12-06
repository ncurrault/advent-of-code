import re
import string

PRACTICE = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()

MARKER_LEN = 14

for i in range(MARKER_LEN, len(file_content) + 1):
    last_four = file_content[i - MARKER_LEN : i]
    if len(set(last_four)) == MARKER_LEN:
        print(i)
        break
