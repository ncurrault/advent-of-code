from collections import defaultdict
import re
import string

PRACTICE = True
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()

lines = file_content.split("\n")
