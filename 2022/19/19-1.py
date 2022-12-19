import string
import re
import math
from collections import defaultdict
from enum import Enum
import itertools
import tqdm

PRACTICE = True
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()
lines = file_content.split("\n")
