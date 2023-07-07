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
import pandas as pd

PLOT_SIZE_LIMIT = 10
# This should be half of the interval between writes.
# See logger.py.
GET_LINE_DELAY_S = 0.05

# File name.
gDataFilename = ""
# Data to plot.
gFigure = None
gRPMAxes = None
gCofAxes = None
gPlotTime = []
gPlotRPM = []
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


def update_axes_from_file():
    global gDataFilename, gPlotTime, gPlotRPM, gPlotFriction
    data = pd.read_csv(gDataFilename)
    gPlotTime = data["Time"]
    gPlotRPM = data["RPM"]
    gPlotFriction = data["Coefficient of friction"]


def plot_rpm():
    global gRPMAxes
    # Plot the RPM
    gRPMAxes.clear()
    gRPMAxes.set_title("RPM Against Time")
    gRPMAxes.set_xlabel("Time (seconds)")
    gRPMAxes.set_ylabel("RPM")
    # Rotate X axis labels.
    labels = gRPMAxes.get_xticklabels()
    plt.setp(labels, rotation=45, horizontalalignment="right")
    # Plot the values.
    gRPMAxes.plot(gPlotTime, gPlotRPM, "r")


def plot_cof():
    global gCofAxes
    # Plot the coefficient of friction
    gCofAxes.clear()
    gCofAxes.set_title("Friction Coefficient Against Time")
    gCofAxes.set_xlabel("Time (seconds)")
    gCofAxes.set_ylabel("Friction coefficient")
    # Rotate X axis labels.
    labels = gCofAxes.get_xticklabels()
    plt.setp(labels, rotation=45, horizontalalignment="right")
    # Plot the values.
    gCofAxes.plot(gPlotTime, gPlotFriction, "b")


# The parameter is a frame count that we don't use.
def update_plot(_):
    update_axes_from_file()
    # Plot the data.
    plot_rpm()
    plot_cof()


def start_plotting():
    global gFigure, gRPMAxes, gCofAxes
    # Set style
    plt.style.use("fivethirtyeight")
    # Set up figure and axes.
    gFigure, (gRPMAxes, gCofAxes) = plt.subplots(
        figsize=(8, 8),
        nrows=2,
        ncols=1,
    )
    gFigure.set_tight_layout(True)
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
