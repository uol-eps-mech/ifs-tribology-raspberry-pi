# IFS Tribology Lab Raspberry Pi Data Logger

Information about setting up and using Raspberry Pis in the Tribology lab.

STUDENTS - There is a README file in the home directory called
"STUDENTS_READ_THIS_FILE.md" that explains how to use this.

The rest of this files is for the maintainers of this project.

Raspberry Pi 4Bs are used for most of the machines in the Tribology lab and most are setup the same way.

Type A and Type B variants have

* 2 x BNC connectors for +/-10V voltage inputs.
* 2 x K type thermocouple inputs.

In addition, the type A has a 9 way D-Sub for monitoring the rotational speed reported by the pendulum tribometer.

## Setup and testing

To setup the RPi software, see [this document](setup_rpi.md).  Once that is done, install this repo as follows:

```bash
cd ~
git clone https://github.com/uol-eps-mech/ifs-tribology-raspberry-pi.git
```

Then run the software:

```bash
cd ~/ifs-tribology-raspberry-pi/code
./start.bash
```

There are some notes and photos on how the hardware is put together [here](construction/construction.md).

There are some notes on testing the final boxes [here](testing.md).

I also wrote some [design notes](design.md) for the software.

## License

This work is licensed under the MIT licence.  See LICENSE file for details.

© 2023-2024, University of Leeds.

The author, A. Blight, has asserted his moral rights.
