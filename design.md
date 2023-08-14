# Design notes

The software for this project is formed of three main parts:

1. The MCC DAQ examples.  These just work and do a fair bit of what we need.
2. Initial code started by Jack Rudd with a little polishing by me.
3. The final version of code.

All of the code can be found in the `code` directory.  The first versions of the code (in the `intern` directory ) were developed to get the system working and are a little rough around the edges.  They did the job but had the problem that the data was written to disk in 4k blocks.  If the program was stopped before that, the data would be lost.  This caused by the abrupt exit of the program that prevented us from calling a function to flush the buffer to disk.

After many hours of research and a lot of testing, I found [this answer on StackOverflow](https://stackoverflow.com/questions/72697369/real-time-data-plotting-from-a-high-throughput-source).  This does the classic separation of concerns thing by splitting the problem into two parts:

1. Data acquisition and recording.
2. Presentation of the data.

Some programs I developed during this testing are in the `code/trial` directory.  After some more attempts at doing this on a single file that failed, I implemented two programs started by a Bash script.  The results can be found in the `code` directory.

## Pendulum Tribometer Motor characteristics

The motor has a maximum speed of 1800RPM and a minimum speed of about 70RPM.  This means that if the last interrupt occurred more than 1 second ago, the motor is off so the speed is 0RPM.

The pendulum tribometer test rotor are connected to the motor shaft using a toothed belt.  The gear wheel on the motor shaft has 25 teeth and the gear wheel connect to the test rotor has 47 teeth.  The effective gear ration is: 25:47 or 1.88:1.

