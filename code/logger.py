#!/usr/bin/env python3

import time
import random

# Data generator.

LIMIT_TIME = 100  # s
DATA_FILENAME = "data.txt"


def gen_data(filename, limit_time):
    start_time = time.time()
    elapsed_time = time.time() - start_time
    with open(filename, "w") as f:
        while elapsed_time < limit_time:
            f.write(f"{time.time():30.12f} {random.random():30.12f}\n")  # produces 64 bytes
            f.flush()
            elapsed_time = time.time() - start_time

gen_data(DATA_FILENAME, LIMIT_TIME)
