#!/usr/bin/env python3

"""
Generate a revolutions per minute value from the rotary encoder.

An interrupt driven callback calculates the time taken between the current
interrupt and the last interrupt.  This time difference is then used to
calculate the RPM value that can be read by another process.
"""

import signal
import sys
import time
import RPi.GPIO as GPIO
from datetime import datetime
from threading import Thread


ENCODER_Z_GPIO = 22

# 25 teeth on motor, rotor end has 47.
ROTOR_RATIO = 25.0 / 47.0


class Encoder:
    def __init__(self) -> None:
        self._rpm = 0.0
        self._last_datetime = datetime.now()
        GPIO.setmode(GPIO.BCM)
        # External pull up resistors are fitted.
        GPIO.setup(ENCODER_Z_GPIO, GPIO.IN)
        GPIO.add_event_detect(
            ENCODER_Z_GPIO, GPIO.FALLING, callback=self.interrupt_callback
        )

    def get_rpm(self) -> float:
        # Motor minimum speed is about 70RPM, so interrupts should be less then 1 second apart.
        # If the last interrupt was more than 1 second ago the motor has stopped.
        delta = datetime.now() - self._last_datetime
        rpm = self._rpm
        if delta.total_seconds() > 1.0:
            rpm = 0.0
        return rpm

    def interrupt_callback(self, channel) -> None:
        # Each interrupt happens exactly once per revolution.
        now = datetime.now()
        # print(now)
        delta = now - self._last_datetime
        # Convert to RPM.
        self._rpm = (1.0 / delta.total_seconds()) * 60
        # Save now for later...
        self._last_datetime = now


def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)


def print_loop() -> None:
    print("Loop started")
    encoder = Encoder()
    while True:
        time.sleep(1.0)
        rpm = encoder.get_rpm()
        rotor_rpm = rpm * ROTOR_RATIO
        print("Motor = {}RPM, rotor {}RPM ".format(rpm, rotor_rpm))


def main() -> None:
    print_thread = Thread(target=print_loop)
    print_thread.start()
    signal.signal(signal.SIGINT, signal_handler)
    #  The program waits until killed when pause() is called.
    signal.pause()


if __name__ == "__main__":
    print("Started")
    main()
    print("Done")
