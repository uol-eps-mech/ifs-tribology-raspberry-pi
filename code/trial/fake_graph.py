#!/usr/bin/env python3
""" This file provides a data logging program for the Pendulum Tribometer.
The data source should be an MCC-118 DAQ card but this file uses a fake
data source to allow it to be run on a PC.
"""

# Importing libraries
import sys

# from daqhats import hat_list, HatIDs, mcc118
import time
import numpy as np
import threading
import math
from datetime import datetime
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

# File name.  Change this.

FILE_NAME="nogreasetest41rpm.txt"


plot_friction = []
plot_time = []


class FakeMCC118DAQ:
    """A fake version of the MCC-118 DAQ class that returns a value with some
    random noise on it so that some changes are visible.
    """

    def __init__(self):
        pass

    def read_value(self):
        """Return a value of 1.5V plus or minus 0.5V of simulated noise."""
        value = 1.0 + random.random()
        return value


class DataReader(threading.Thread):
    def __init__(self):
        self.file = None
        self.board = FakeMCC118DAQ()
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()

    def stop(self):
        print("Called stop")
        self._stop_event.set()

    def is_stopped(self):
        return self._stop_event.is_set()

    def open_file():
        """Open file to store results."""
        self.file = open(FILE_NAME, "a")

    def convert_data(self, value):
        voltage = value + 0.3  # Value taken from the difference at 0
        angle_DEG = (
            voltage
        ) * 9.5  # Calibration value taken experimentally from the pendulum
        angle_RAD = (angle_DEG * 3.14159265) / 180
        c_o_f = abs(math.sin(angle_RAD)) / (
            math.tan(1.0472)
        )  # Processing angle data to Friction data
        return (voltage, angle_DEG, c_o_f)

    def append_to_plot(self, now, c_o_f):
        global plot_time, plot_friction
        plot_time.append(now.timestamp())
        plot_friction.append(c_o_f)

    # Writing data function
    def write_data_to_file(t, v, a, f):
        time = t
        voltage = str(round(v, 3))
        angle = str(round(a, 2))
        friction = str(round(f, 3))
        self.file.write(time + "\t" + voltage + "\t" + angle + "\t" + friction)
        self.file.write("\n")


    def run(self):
        global plt
        try:
            while True:
                raw_value = self.board.read_value()
                data = self.convert_data(raw_value)
                voltage = data[0]
                angle_DEG = data[1]
                c_o_f = data[2]
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                # Prints the raw data value
                print(
                    "{}: Ch {}: {:.3f}: Angle {}".format(
                        current_time, 0, raw_value, angle_DEG
                    )
                )
                # Writes file data
                self.write_data_to_file(current_time, voltage, angle_DEG, c_o_f)
                self.append_to_plot(now, c_o_f)
                # Need to break loop to close file
                time.sleep(0.2)
        except KeyboardInterrupt:
            pass
        print("Thread stopped")
        plt.close("all")
        print("Closing file")
        self.file.flush()
        self.file.close()



def openplotwindow():
    # Initialise plot style
    global plt
    plt.style.use("fivethirtyeight")


# Defining animate function for graph which reads, processes and saves the data
def animate(i):
    global plot_time, plot_friction
    plt.cla()
    plt.plot(plot_time, plot_friction)
    plt.title("Friction Coefficient Against Time")
    plt.xlabel("Time [seconds]")
    plt.ylabel("Friction coefficient")


def main():
    print("Starting thread...")
    reader = DataReader()
    reader.open_file()
    # Start thread.  Calls DataReader.run() after doing thread things.
    reader.start()
    print("Starting plot...")
    openplotwindow()
    ani = FuncAnimation(
        plt.gcf(), animate, interval=10
    )  # Animating the graph to update for every new data set
    plt.tight_layout()
    # plt.show never ends unless plt.close is used.
    plt.show()


main()

# tidyup()
