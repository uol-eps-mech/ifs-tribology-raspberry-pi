# Raspberry Pi Set Up

How to setup the Raspberry Pi 4.

## Use the pre-built image

This is by far the quickest way.  The current image has all (except Eduroam) of the below ready to go an install in about 5 minutes.  The image file can be installed as follows:

### Pre-requisites

1. IMPORTANT. You need a PC that is not locked down by IT as you need Admin privileges to write to an SD card.  I use a laptop running Kubuntu.
2. The image file and copy somewhere on your PC that you can find easily.  The latest image file can be obtained from Andy Blight.
3. The Raspberry Imager software installed and ready to use.  Get it from: <https://www.raspberrypi.com/software/>
4. A micro SD card to install the OS on. The cards we use are SanDisk Extreme A2 64 GB.  The fast speeds are important when running on a Raspberry Pi.

### Installation

These instructions were run on Kubuntu 22.04LTS.

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

The version we are using is the latest Raspberry Pi OS (32 bit) installed following the instructions here: <https://www.raspberrypi.com/software/>. To summarise:

1. Install the Raspberry Pi Imager tool.
2. Insert SD Card.  I used this [SD card](https://www.amazon.co.uk/SanDisk-microSDHC-Adapter-Performance-SDSQUA4-032G-GN6MA/dp/B08GY9NYRM/).  Gold ones like [this](https://www.amazon.co.uk/SanDisk-Extreme-microSDHC-Adapter-Performance/dp/B06XWMQ81P/) are better!
3. On the imager tool, select
   1. The recommended desktop image (about 1.2GB).
   2. The SD card.
   3. Then press `Write` and wait a while (took about 20 minutes or so).  The imager downloads the image, writes it to the SD card and then verifies the image.
4. When done, eject the SD card.

## Set up the new OS

Insert the SD card into the Raspberry Pi, make sure a keyboard, mouse and and HDMI monitor is connected, then apply power.  After a while, you will get a nice picture of a sunset and a little dialog box that tells you to set up a a few things.  This is what I did:

1. Press `Next`.
2. Set Country.  The default options are for the UK so I left them alone. Press `Next`.
3. Enter a new user name (pi) and password, then press `Next`.
4. Set the screen black bars option as appropriate. Press `Next`.
5. Connect to Wi-Fi.  If you are at the University and connecting to Eduroam, press `Skip`.  Otherwise, select the Wi-Fi and press `Next`.  Then enter the Wi-Fi password and press `Next`.
6. Update Software.  Press `Skip` if no Wi-Fi, or `Next` to update.  The software update will take an hour or so, so I prefer to skip this step and do the update later.
7. Press `Restart`.

After restarting, we need to start customising our Pi.

1. Enable SSH for remote editing and SPI to communicate with the ADC AD7124 device.
   1. Open a new terminal window.
   2. Enter: `sudo raspi-config`
   3. Select `3. Interface options`.
   4. Select `P2 SSH` option and enable.
   5. Select `P4 SPI` option and enable.
   6. Escape back to start page and exit.
   7. Verify that you can connect to the Pi using SSH.
      1. On the Pi, enter this command `ip addr`.  Note the IPv4 address, e.g. `192.168.2.179`.
      2. Open new shell on your Ubuntu PC.
      3. Enter `ssh pi@192.168.54.179`.
      4. The first time you do this, you will be asked to authenticate the new SSH entry.  Enter `yes`.
      5. You should be asked for the `pi` user password and then a shell will appear.
   8. Now verify that the SPI bus is enabled.  Using a terminal shell on the Pi, list the `/dev` directory and you should see two entries like this:

      ```bash
      ls /dev/spi*
      /dev/spidev0.0  /dev/spidev0.1
      ```

   9. Now to add a few useful tools.
      1. Execute these commands:

          ```bash
          cd
          git clone https://github.com/andyblight/bash_scripts.git
          ```

          A new directory will be created called `bash_scripts`.
      2. Now run the following commands:

          ```bash
          cd ~/bash_scripts
          ./install.sh ubuntu18.04lts
          cd ubuntu18.04lts/desktop-installs/
          ./install-git-tools.sh
          ```

        This will install some tools that I find useful when working on Debian/Ubuntu PCs and the Raspberry Pi.  The tools are:

        * `vim` a command line text editor.
        * `gitk` a viewer for the hsitory of a `git` repo.
        * Some custom `Bash` enhancements in `~/.bash_aliases`.
        * Some `git` aliases in `~/.gitconfig`.
        * A nice system update script.

   10. Start a new terminal shell to pick up the enhancements from the `Bash` aliases.
   11. Now that most of the setup has been done, it is time to do that update that you've been putting off.  Time to run the system update script.  In a terminal windows on the RPi, run `upgrade.sh` and let it go!  A full update may take up to an hour, so be prepared to wait.

## Eduroam

This is documented [here](https://github.com/RealRobotics/rpi-kb/blob/main/eduroam/eduroam.md).

## Setup software for the MCC DAQ cards

The MCC
