#!/bin/bash
# Start the two programs that are used for the Tribometer data logger.
# The graph program is run in the background but can be stopped using the buttons on the GUI.

DATA_FILE_NAME="${1:data.csv}"

python3 plotter.py ${DATA_FILE_NAME} &
python3 logger.py ${DATA_FILE_NAME}
