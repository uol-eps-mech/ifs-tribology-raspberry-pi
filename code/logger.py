#!/usr/bin/env python3

""" A program that logs data from the Pendulum Tribometer.
    Currently only supports a single channel, channel 0.
"""

import math
import os
import sys
import time
import random
from datetime import datetime
from argparse import ArgumentParser
from daqhats import hat_list, HatIDs, mcc118
import RPi.GPIO as GPIO

# The interval between each reading in seconds.
INTERVAL_S = 0.1
CSV_HEADER_STRING = "Time,RPM,Voltage,Angle Degrees,Coefficient of friction\n"

# GPIO pin for the encoder.
ENCODER_Z_GPIO = 22

# Plate on back says max speeds are:
# Fast shaft = 1800. This is what the encoder reports.
# Slow shaft speed = 417.  This is the outpu from the gearbox.
MOTOR_GEARBOX_RATIO = 417 / 1800

# 25 teeth on motor, rotor end has 47.
BELT_RATIO = 25 / 47

# Value to divide the encoder pulses by to get the rotor speed.
ROTOR_RATIO = MOTOR_GEARBOX_RATIO * BELT_RATIO

# Maximum RPM of motor is 1800rpm.
MAX_MOTOR_RPM = 1800

# Input voltage offset. The value being read it is not always zero
# when the pendulum is centred, so change this value as needed.
PENDULUM_OFFSET_VOLTAGE = 0.0

def convert_voltage_to_values(voltage_v):
    """ Converts the input voltage into an angle and then into a
    co-efficent of friction value.
    """
    # Convert reading into a tuple of values.
    corrected_voltage_v = voltage_v + PENDULUM_OFFSET_VOLTAGE
    # Calibration value taken experimentally from the pendulum.
    angle_DEG = (corrected_voltage_v) * 9.5
    angle_RAD = (angle_DEG * 3.14159265) / 180
    # Processing angle data to Friction data
    coefficient_of_friction = abs(math.sin(angle_RAD)) / (math.tan(1.0472))
    return (corrected_voltage_v, angle_DEG, coefficient_of_friction)


# class FakeMCC118DAQ:
#     """A fake version of the MCC-118 DAQ class that returns a value with some
#     random noise on it so that some changes are visible.
#     """

#     def __init__(self):
#         pass

#     def get_reading(self, channel):
#         """Return a value simulating a voltage.
#         Each channel has a different central voltage.
#         """
#         if channel == 0:
#             value = 1.0 + random.random()
#         elif channel == 1:
#             value = 2.0 + random.random()
#         # Convert reading into a tuple of values.
#         # Value taken from the difference at 0
#         voltage = value + 0.3
#         # Calibration value taken experimentally from the pendulum.
#         angle_DEG = (voltage) * 9.5
#         angle_RAD = (angle_DEG * 3.14159265) / 180
#         # Processing angle data to Friction data
#         coefficient_of_friction = abs(math.sin(angle_RAD)) / (math.tan(1.0472))
#         return (voltage, angle_DEG, coefficient_of_friction)


class MCC118DAQ:
    """Provides functions to use the MCC-118 DAQ hat."""

    def __init__(self):
        self.board = None
        self.board_list = hat_list(filter_by_id=HatIDs.ANY)
        if not self.board_list:
            print("No boards found")
            sys.exit()
        else:
            for entry in self.board_list:
                if entry.id == HatIDs.MCC_118:
                    self.board = mcc118(entry.address)
                    break

    def get_voltage(self, channel):
        """Return the voltage in Volts for the given channel."""
        voltage_v = 0.0
        if channel == 0 or channel == 1:
            voltage_v = -1.0 * self.board.a_in_read(channel)
        return voltage_v


# class FakeEncoder:
#     def __init__(self):
#         pass

#     def get(self):
#         # Fake value for now.
#         rpm = 25.0 + (random.random() * 0.5)
#         return rpm

#     def close(self):
#         pass


class Encoder:
    def __init__(self) -> None:
        self._rpm = 0.0
        self._last_datetime = datetime.now()
        GPIO.setmode(GPIO.BCM)
        # External pull up resistors are fitted.
        GPIO.setup(ENCODER_Z_GPIO, GPIO.IN)
        GPIO.add_event_detect(ENCODER_Z_GPIO, GPIO.FALLING, callback=self.interrupt_callback)

    def get_rpm(self) -> float:
        return self._rpm

    def interrupt_callback(self, channel) -> None:
        # Each interrupt happens exactly once per revolution.
        now = datetime.now()
        # print(now)
        # Calculate interval between last interrupt and this one.
        delta = now - self._last_datetime
        # Motor minimum speed is about 70RPM, so interrupts should be less then 1 second apart.
        # If the last interrupt was more than 1 second ago the motor has stopped.
        if delta.total_seconds() > 1.0:
            self._rpm = 0.0
        else:
            # Convert delta time to RPM.
            new_rpm = (1.0 / delta.total_seconds()) * 60
            # print("new_rpm {}".format(new_rpm))
            # Some values produced are completely wrong, possibly caused
            # by electrical noise.
            if new_rpm <= MAX_MOTOR_RPM:
                self._rpm = new_rpm
        # Save now for later...
        self._last_datetime = now


class Logger:
    def __init__(self):
        # Start the encoder driver.
        # self._encoder = FakeEncoder()
        self._encoder = Encoder()
        # Start the DAQ driver.
        # self._daq = FakeMCC118DAQ()
        self._daq = MCC118DAQ()
        self._running = True
        # Record start epoch time.
        self._start_time = time.time()

    def _get_formatted_output(self):
        # Get RPM.
        motor_rpm = self._encoder.get_rpm()
        rotor_rpm = motor_rpm * ROTOR_RATIO
        # Get data from channel 0.  Change to 1 if needed.
        voltage_v = self._daq.get_voltage(0)
        voltage, angle_DEG, coefficient_of_friction = convert_voltage_to_values(voltage_v)
        # Get the time since program started in seconds.
        duration = time.time() - self._start_time
        # Create formatted string.
        output_string = "{:.3f},{:.3f},{:.3f},{:.3f},{:.3f}\n".format(
            duration, rotor_rpm, voltage, angle_DEG, coefficient_of_friction
        )
        # Debug. Can comment out if annoying.
        print(output_string)
        return output_string

    def run(self, filename, interval_s):
        with open(filename, "w") as logger_file:
            # Write header.
            print(CSV_HEADER_STRING)
            logger_file.write(CSV_HEADER_STRING)
            try:
                while True:
                    output_string = self._get_formatted_output()
                    logger_file.write(output_string)
                    # Make sure the data are written immediately.
                    logger_file.flush()
                    time.sleep(interval_s)
            except KeyboardInterrupt:
                print("Stopped by user")


def get_args():
    parser = ArgumentParser()
    parser.add_argument("filename", help="write report to FILE", metavar="FILE")
    return parser.parse_args()


def main():
    args = get_args()
    logger = Logger()
    logger.run(args.filename, INTERVAL_S)
    os.sync()


if __name__ == "__main__":
    main()
