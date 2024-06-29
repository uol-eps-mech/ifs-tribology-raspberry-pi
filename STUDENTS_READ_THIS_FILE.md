# How to use the Raspberry Pi Data Logger software

## Temperature recording

 TO DO.

## Pendulum Tribometer software

The Pendulum Tribometer software records the following information:

* The speed of the test rotor in RPM.
* The voltage sent from the charge amplifier.
* The angle of the test arm from 0, calculated from the input voltage.
* The coefficient of friction, calculated from the angle.

These data are output into a CSV file for later analysis.

### Running the Pendulum Tribometer software

To run the software, type the following commands in a terminal window.

```bash
cd ~/ifs-tribology-raspberry-pi/code
./start.bash
```

These commands will start two programs.  The first program is `logger.py`
that logs data from the pendulum tribometer to a CSV file.  The second
program is a graph plotting program `plotter.py`.  This program is only
intended to allow you to see roughly what is going on and
__THE GRAPHS ARE NOT STORED__.

The default name of the CSV file is "data.csv" but you can change
this as follows:

```bash
 ./start.bash my_file_name.csv
```

In this example, the data will be written to the file `my_file_name.csv`.

PLEASE NOTE: If you use the same data file name more than once, the previous
data file will be deleted and a new file will be written to.

To plot a graph of the data, you need to copy the CSV files that the logger
program creates onto a USB memory stick and then use Excel or similar
to create the plots that you need.

## Date and time

The Raspberry Pi normally updates the date and time from the internet.
To prevent hackers mis-using the Raspberry Pi, __the data loggers are not
connected to the internet__.  This means that the date and time are nearly
always wrong.  It would be a good idea to record the time shown on
the data logger in your log book or similar so that you know when each
test run was done and what time the data logger was showing.
