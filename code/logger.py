#!/usr/bin/env python3
import os
import time
import random
from datetime import datetime

# The interval between each reading in milliseconds.
INTERVAL_MS = 100
DATA_FILENAME = "data.csv"
# Output format. 1 for CSV else 0.
OUTPUT_FORMAT_CSV = 1


class FakeMCC118DAQ:
    """A fake version of the MCC-118 DAQ class that returns a value with some
    random noise on it so that some changes are visible.
    """

    def __init__(self):
        pass

    def get(self, channel):
        """Return a value simulating a voltage.
        Each channel has a different central voltage.
        """
        if channel == 0:
            value = 1.0 + random.random()
        elif channel == 1:
            value = 2.0 + random.random()
        return value


class Encoder:
    def __init__(self):
        pass

    def get(self):
        # Fake value for now.
        rpm = 25.0 + (random.random() * 0.5)
        return rpm

    def close(self):
        pass


class Logger:
    def __init__(self):
        self._encoder = Encoder()
        self._daq = FakeMCC118DAQ()
        self._running = True

    def _voltage_to_friction(self, voltage):
        # TODO some clever conversion.
        return voltage

    def _get_formatted_output(self):
        # Get data.
        voltage_0 = self._daq.get(0)
        friction_0 = self._voltage_to_friction(voltage_0)
        voltage_1 = self._daq.get(1)
        friction_1 = self._voltage_to_friction(voltage_1)
        rpm = self._encoder.get()
        now = datetime.now()
        now_string = now.strftime("%H:%M:%S.%f")
        # Create formatted string.
        if OUTPUT_FORMAT_CSV == 0:
            output_string = "{}: RPM: {}, Angle 1: {}, Angle 2: {}\n".format(
                now_string, rpm, friction_0, friction_1
            )
        else:
            output_string = "{},{},{},{}\n".format(
                now_string, rpm, friction_0, friction_1
            )
        # Debug. Can comment out if annoying.
        print(output_string)
        return output_string

    def run(self, filename, interval_ms):
        with open(filename, "w") as logger_file:
            if OUTPUT_FORMAT_CSV == 1:
                # Write header.
                header_string = "Time,RPM,Angle 1,Angle 2\n"
                print(header_string)
                logger_file.write(header_string)
            try:
                while True:
                    output_string = self._get_formatted_output()
                    logger_file.write(output_string)
                    time.sleep(interval_ms / 1000)
            except KeyboardInterrupt:
                print("Stopped by user")


def main():
    logger = Logger()
    logger.run(DATA_FILENAME, INTERVAL_MS)
    os.sync()


if __name__ == "__main__":
    main()
