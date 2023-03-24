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
        self.graph = plt.figure()
        self.graph.tight_layout()
        self.ax = self.graph.add_subplot(111)
        self.ax.set_ylim(-1, 1)
        self.ax.set_xlim(0, 10)
        # prints running simulation time
        self.time_template = "Time = %.1f s"
        self.time_text = self.ax.text(0.05, 0.9, "", transform=self.ax.transAxes)
        # Animating the graph to update for every new data set
        self.animation = FuncAnimation(
            self.graph, self.simPoints, self.simData, blit=False, interval=10, repeat=True
        )

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
        return self.line, self.time_text


    def run(self):
        """Start the plotting thread"""
        self.graph.show()

    def start(self):
        self.animation.start()

    def stop(self):
        self.animation.stop()


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
