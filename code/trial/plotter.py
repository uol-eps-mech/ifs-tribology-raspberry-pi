#!/usr/bin/env python3

import time
import io
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


BUFFER_LEN = 64
DATA_FILENAME = "data.txt"
PLOT_LIMIT = 20
ANIM_FILENAME = "video.gif"


fig, ax = plt.subplots(1, 1, figsize=(10,8))
ax.set_title("Plot of random numbers from `gen.py`")
ax.set_xlabel("time / s")
ax.set_ylabel("random number / #")
ax.set_ylim([0, 1])


def get_data(filename, buffer_len, delay=0.0):
    with open(filename, "r") as f:
        f.seek(0, io.SEEK_END)
        data = f.read(buffer_len)
        if delay:
            time.sleep(delay)
    return data


def animate(i, xs, ys, limit=PLOT_LIMIT, verbose=False):
    # grab the data
    try:
        data = get_data(DATA_FILENAME, BUFFER_LEN)
        if verbose:
            print(data)
        x, y = map(float, data.split())
        if x > xs[-1]:
            # Add x and y to lists
            xs.append(x)
            ys.append(y)
            # Limit x and y lists to 10 items
            xs = xs[-limit:]
            ys = ys[-limit:]
        else:
            print(f"W: {time.time()} :: STALE!")
    except ValueError:
        print(f"W: {time.time()} :: EXCEPTION!")
    else:
        # Draw x and y lists
        ax.clear()
        ax.set_ylim([0, 1])
        ax.plot(xs, ys)


# show interactively
print("Starting animation.")
anim = FuncAnimation(fig, animate, fargs=([time.time()], [None]), interval=1)
plt.show()
print("After show.")
plt.close()
print("Done.")
