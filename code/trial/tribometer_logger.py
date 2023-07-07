#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
    Reads the encoder and the two voltage inputs.
    The voltages are converted to friction values and the data are written to
    a specified file.
    Also shows the RPM and the voltages on a graph.
"""
import time
import random
from threading import Thread
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime


class EncoderLogger:
    def __init__(self):
        pass

    def get(self):
        # Fake value for now.
        rpm = 25.0 + (random.random() * 0.5)
        return rpm

    def close(self):
        pass


class VoltageLogger:
    def __init__(self, input):
        self._input = float(input)

    def get(self):
        # Fake value for now.
        voltage = self._input + (random.random() * 0.5)
        return voltage

    def close(self):
        pass


class LoggerThread(Thread):
    def __init__(self):
        self._encoder_logger = EncoderLogger()
        self._voltage_logger_1 = VoltageLogger(1)
        self.voltage_logger_2 = VoltageLogger(1)
        self._running = True

    def close(self):
        self._voltage_logger_2.close()
        self._voltage_logger_1.close()
        self._encoder_logger.close()

    def _voltage_to_friction(self, voltage):
        # TODO some clever conversion.
        return voltage

    def _write_data_to_file(self, time, rpm, friction_1, friction_2):
        # For now, print data to stdoout.
        print(
            "{}: RPM: {}, Angle 1: {}, Angle 2: {}".format(
                time, rpm, friction_1, friction_2
            )
        )

    def run(self):
        """This function over-rides the one from the Thread class."""
        try:
            while self._running:
                voltage_1 = self._voltage_logger_2.get()
                friction_1 = self.convert(voltage_1)
                voltage_2 = self._voltage_logger_1.get()
                friction_2 = self.convert(voltage_2)
                rpm = self._encoder_logger.get()
                now = datetime.now()
                now_string = now.strftime("%H:%M:%S")
                self._write_data_to_file(now_string, rpm, friction_1, friction_2)
                time.sleep(1.0)
        except KeyboardInterrupt:
            pass


class GraphPlotter:
    def __init__(self):
        # Lists of data points for the graph.
        self._plot_time = []
        self._plot_rpm = []
        self._plot_friction_1 = []
        self._plot_friction_2 = []
        # Animating the graph to update for every new data set
        self._ani = FuncAnimation(plt.gcf(), self.animate, interval=10)
        plt.tight_layout()

    def add_data(self, time, rpm, friction_1, friction_2):
        self._plot_time.append(time)
        self._plot_rpm.append(rpm)
        self._plot_friction_1.append(friction_1)
        self._plot_friction_2.append(friction_2)

    def animate(self):
        plt.cla()
        plt.plot(
            self._plot_time,
            self._plot_rpm,
            self._plot_friction_1,
            self._plot_friction_2,
        )
        plt.title("Friction Coefficient Against Time")
        plt.xlabel("Time [seconds]")
        plt.ylabel("Friction coefficient")

    def run(self):
        # plt.show never ends unless plt.close is used.
        plt.show()


def main():
    logger = LoggerThread()
    logger.start()
    print("Logger started")
    # This function blocks until the graph is closed.
    graph_plotter = GraphPlotter()
    graph_plotter.run()
    # Close down the logger to write all data to the files.
    print("Waiting for the logger to finish")
    logger.join()


if __name__ == "__main__":
    main()
