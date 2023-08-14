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


ENCODER_Z_GPIO = 4


class Encoder:
    def __init__(self) -> None:
        self._rpm = 0.0
        self._last_datetime = datetime.now()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(ENCODER_Z_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(
            ENCODER_Z_GPIO, GPIO.RISING, callback=self.interrupt_callback, bouncetime=200
        )

    def get_rpm(self) -> float:
        return self._rpm

    def interrupt_callback(self, channel) -> None:
        print("ISR called")
        # Each interrupt happens exactly once per revolution.
        now = datetime.now()
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
        print("RPM = {}".format(rpm))


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
