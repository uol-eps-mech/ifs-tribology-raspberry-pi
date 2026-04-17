# Raspberry Pi Set Up

How to setup the Raspberry Pi 4.

## Use the pre-built image

This is by far the quickest way.  The current image has all (except Eduroam) of the below ready to go an install in about 5 minutes.  Andy Blight knows where the images are (on his PC and backed up on the IT provided Globus file store).  The current image is `tribology_rpi_20250305.img.gz`.  The image file can be installed as follows.

### Pre-requisites

1. IMPORTANT. You need a PC that is not locked down by IT as you need Admin privileges to write to an SD card.  I use a laptop running Kubuntu.
2. The image file and copy somewhere on your PC that you can find easily.  The latest image file can be obtained from Andy Blight.
3. The Raspberry Imager software installed and ready to use.  Get it from: <https://www.raspberrypi.com/software/>
4. A micro SD card to install the OS on. The cards we use are SanDisk Extreme A2 64 GB.  The fast speeds are important when running on a Raspberry Pi.

### Installation

These instructions were run on Kubuntu 24.04LTS but should work on a Windows PC (if you have admin access).

1. Insert the micro SD card into you PC.  You may need an SD to micro SD card adapter.
2. Open the Raspberry Pi Imager program.
3. Click on the `Operating System` button.
4. Scroll to the bottom of the list and click on `Use custom`.
5. Navigate to the place you stored the image file, select it and press `Open`.
6. Press the `Storage` button.
7. Click on the SD card to use.
8. Press the `Write` button.
9. Press `Yes` when the next dialog box comes up.
10. Enter your PC password when prompted.
11. The imager program will then write the image to the card, verify the image.  This takes a few minutes.
12. When complete, a dialog pops up to tell you to remove the SD card, so do it and you're done!

## Download and install the OS

This is the hard way!

The version we are using is the Raspberry Pi OS, Debian Trixie (64 bit) release (2026-04-13) installed using the instructions here: <https://www.raspberrypi.com/software/>. To summarise:

1. Install the Raspberry Pi Imager tool.
2. Insert SD Card.  I used this [SD card](https://www.amazon.co.uk/SanDisk-microSDHC-Adapter-Performance-SDSQUA4-032G-GN6MA/dp/B08GY9NYRM/).  Gold ones like [this](https://www.amazon.co.uk/SanDisk-Extreme-microSDHC-Adapter-Performance/dp/B06XWMQ81P/) are better!
3. On the imager tool, select
   1. The full desktop image.
   2. The SD card.
   3. Then press `Write` and wait a while (took about 20 minutes or so).  The imager downloads the image, writes it to the SD card and then verifies the image.
4. When done, eject the SD card.

## Set up the new OS

Insert the SD card into the Raspberry Pi, make sure a keyboard, mouse and and HDMI monitor is connected, then apply power.  After a while, you will be prompted to create a user and password.

User: `logger`
Password: `tribology`

Then select language and keyboard layout, British English for both, and then set up wi-fi to connect to the local RR lab network.

Once the main screen comes up, open a terminal shell and run `sudo raspi-config`, enable `SSH` and exit.  Verify that you can access the RPi from you PC using SSH.

## Setup software for the MCC DAQ cards

This is fairly simple.  Clone the local version of the MCC-DAQ hats repo (it has some fixes on it for GTK 3.16 and later) and build the code.

```bash
cd ~
git clone git@github.com:uol-eps-mech/daqhats.git
cd ~/daqhats
sudo ./install.sh
sudo pip install -break-system-packages daqhats
sudo daqhats_read_eeproms
```

If you are using new DAQ hats, you may need to update the firmware on them.  Instructions for this can be found in the file `~/daqhats/README`.

To build the thermocouple data logger app (from the file `examples/c/mcc134/data_logger/README.md`)

  ```sh
  sudo apt install libgtk-3-dev at-spi2-core autoconf libtool
  ```

Install **GTKDatabox**:

  ```sh
  cd ~
  git clone https://github.com/erikd/gtkdatabox.git
  cd gtkdatabox
  ./autogen.sh
  ./configure
  sudo make install
  ```

Run ldconfig after installing the dependencies.

  ```sh
  sudo ldconfig
  ```

To run the example, enter the following commands:

  ```sh
    cd ~/daqhats/examples/c/mcc134/data_logger/logger
    make
    ./logger
  ```

Check that it start up correctly and that thermocouples return the correct values when plugged into the sockets.

## Clone this repo

Finally, clone this repo:

```bash
cd ~
git clone https://github.com/uol-eps-mech/ifs-tribology-raspberry-pi.git
```

Done! Time for a well deserved cup of tea.
