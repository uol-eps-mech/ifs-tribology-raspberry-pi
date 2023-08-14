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

ENCODER_Z_GPIO = 16


class Encoder:
    def __init__(self) -> None:
        self._rpm = 0.0
        self._last_datetime = datetime.now()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(ENCODER_Z_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(
            ENCODER_Z_GPIO, GPIO.RISING, callback=self.interrupt_callback, bouncetime=10
        )

    def get_rpm(self) -> float:
        return self._rpm

    def interrupt_callback(self, channel) -> None:
        # Each interrupt happens exactly once per revolution.
        delta = datetime.now() - self._last_datetime
        # Convert to RPM
        self._rpm = (1.0 / delta.total_seconds()) * 60


def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)


def main() -> None:
    encoder = Encoder()
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
    while True:
        time.delay(1.0)
        rpm = encoder.get_rpm()
        print("RPM = {}".format(rpm))


if __name__ == "__main__":
    main()
