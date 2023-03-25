#!/bin/bash
# Start the two programs that are used for the Tribometer data logger.
# The graph program is run in the background but can be stopped using the buttons on the GUI.

python3 plotter.py &
python3 logger.py
