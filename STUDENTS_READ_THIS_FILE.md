# How to use the Pendulum Tribometer software

The pendulum tribometer software is installed on this system.
To run the software, type the following commands in a terminal window.

```bash
cd ~/ifs-tribology-raspberry-pi/code
./start.bash
```

These commands will start two programs.  The first program is `logger.py`
that logs data from the pendulum tribometer to a CSV file.  The default name
of the CSV file is "data.csv" but you can change this as follows:

```bash
 ./start.bash my_file_name.csv
```

In this example, the data will be written to the file `my_file_name.csv`.

PLEASE NOTE: If you use the same data file name more than once, the previous
data file will be deleted and a new file will be written to.

The second program to be run is a graph plotting program `plotter.py`.
This program is only intended to allow you to see roughly what is going on
and __THE GRAPHS ARE NOT STORED__.

To plot a graph of the data, you need to copy the CSV files that the logger
program creates onto a USB memory stick and then use Excel or similar
to create the plots that you need.
