#!/usr/bin/env python3
""" This file implements animated graph plotting that can be started and
stopped as needed.
"""

import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class GraphPlotter:
    def __init__(self):
        # Used to stop the plot.
        self.pause = False
        # The graph.
        self.figure = plt.figure()
        self.figure.tight_layout()
        self.ax = self.figure.add_subplot(111)
        self.line, = self.ax.plot([], [], 'bo', ms=10)
        self.ax.set_ylim(-1, 1)
        self.ax.set_xlim(0, 10)
        # prints running simulation time
        self.time_template = "Time = %.1f s"
        self.time_text = self.ax.text(0.05, 0.9, "", transform=self.ax.transAxes)
        self.animation = None
        self.paused = False

    def simData(self):
        # this function is called as the argument for
        # the simPoints function. This function contains
        # (or defines) and iterator---a device that computes
        # a value, passes it back to the main program, and then
        # returns to exactly where it left off in the function upon the
        # next call. I believe that one has to use this method to animate
        # a function using the matplotlib animation package.
        #
        t_max = 10.0
        dt = 0.05
        x = 0.0
        t = 0.0
        while t < t_max:
            x = np.sin(np.pi * t)
            t = t + dt
            yield x, t

    def simPoints(self, simData):
        """ Generate the data to plot. """
        x, t = simData[0], simData[1]
        self.time_text.set_text(self.time_template % (t))
        self.line.set_data(t, x)
        print("data: line {}, text {}".format(self.line, self.time_text))
        return self.line, self.time_text


    def run(self):
        """Start the plotting thread"""
        print("Called show()")
        # Animating the graph to update for every new data set
        self.animation = FuncAnimation(
            self.figure, self.simPoints, self.simData, blit=False, interval=10, repeat=True
        )
        self.animation.ion()
        self.paused = False
        while not self.paused:
            self.animation.show()
            time.sleep(0.1)
        print("exited run loop")
        self.event_source.stop()

    def pause(self, pause):
        print("Called pause()")
        self.paused = True


graph_plotter = GraphPlotter()
graph_plotter.run()
time.sleep(5)
graph_plotter.stop()
time.sleep(1)
graph_plotter.start()
time.sleep(1)
graph_plotter.stop()
time.sleep(1)
graph_plotter.start()
time.sleep(1)
graph_plotter.stop()
