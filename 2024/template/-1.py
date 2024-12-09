import string
import re
import math
from collections import defaultdict
from enum import Enum
import itertools
from tqdm import tqdm, trange
from dataclasses import dataclass
import random
from copy import deepcopy
import os
from pprint import pprint
from typing import Iterable

PRACTICE = True
DEBUG = False
with open("test.txt" if PRACTICE else "input", "r") as f:
    file_content = f.read().strip()
lines = file_content.split("\n")
