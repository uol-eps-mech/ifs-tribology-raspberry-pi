#!/usr/bin/env python3

""" Plots the latest data from the logger script.
Based on these tutorials.
https://matplotlib.org/stable/tutorials/introductory/lifecycle.html
https://matplotlib.org/stable/tutorials/intermediate/tight_layout_guide.html
and these answers:
https://stackoverflow.com/questions/72697369/real-time-data-plotting-from-a-high-throughput-source
https://stackoverflow.com/questions/3290292/read-from-a-log-file-as-its-being-written-using-python
"""

import time
import io
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from argparse import ArgumentParser

PLOT_SIZE_LIMIT = 20
# This should be half of the interval between writes.
# See logger.py.
GET_LINE_DELAY_S = 0.05

# File name.
gDataFilename = ""
# Data to plot.
gFigure = None
gAxes = None
gPlotTime = []
gPlotFriction = []


def get_line(filename: str) -> str:
    line = ""
    with open(filename, "r") as f:
        # Go to the end of the file.
        f.seek(0, io.SEEK_END)
        while True:
            line = f.readline()
            # If line
            if line:
                break
            else:
                # wait a while and try again.
                time.sleep(0.05)
    return line


# The parameter is a frame count that we don't use.
def update_plot(_):
    global gDataFilename, gAxes, gPlotTime, gPlotFriction
    # grab the data
    try:
        line = get_line(gDataFilename)
        # print("Line: '{}'".format(line))
        line = line.rstrip("\n")
        split_line = line.split(",")
        # print("Split Line: {}, '{}'".format(len(split_line), split_line))
        if len(split_line) > 1:
            # Only plot time [0] and coefficient of friction [4].
            gPlotTime.append(split_line[0])
            gPlotFriction.append(split_line[4])
            # Limit size of lists.
            gPlotTime = gPlotTime[-PLOT_SIZE_LIMIT:]
            gPlotFriction = gPlotFriction[-PLOT_SIZE_LIMIT:]
        else:
            print(f"W: {time.time()} :: STALE!")
    except ValueError:
        print(f"W: {time.time()} :: EXCEPTION!")
    else:
        # Plot the two lists on the figure.
        gAxes.clear()
        # Set axes.
        gAxes.set_title("Friction Coefficient Against Time")
        gAxes.set_xlabel("Time [seconds]")
        gAxes.set_ylabel("Friction coefficient")
        # Rotate X axis labels.
        labels = gAxes.get_xticklabels()
        plt.setp(labels, rotation=45, horizontalalignment='right')
        # Set Y axis ticks.
        # gAxes.set_yticks([0, 0.10, 0.20, 0.30, 0.40, 0.50])
        # Plot the values.
        gAxes.plot(gPlotTime, gPlotFriction)


def start_plotting():
    global gFigure, gAxes
    # Set style
    plt.style.use("fivethirtyeight")
    # Set up figure and axes.
    gFigure, gAxes = plt.subplots(figsize=(8, 8))
    # Use tight layout always.
    gFigure.set_tight_layout(True)
    gFigure.text = "My plot"
    # Create animation instance.
    _ = FuncAnimation(fig=gFigure, func=update_plot, interval=10)
    # This function blocks until the user kills it.
    plt.show()
    plt.close()


def get_args():
    parser = ArgumentParser()
    parser.add_argument("filename", help="Plot data from FILE", metavar="FILE")
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser.parse_args()


def main():
    global gDataFilename, gFigure
    args = get_args()
    # print("All args:", args)
    gDataFilename = args.filename
    # show interactively
    print("Starting plotter using file: '{}'".format(gDataFilename))
    start_plotting()
    print("Plotter done.")


if __name__ == "__main__":
    main()
