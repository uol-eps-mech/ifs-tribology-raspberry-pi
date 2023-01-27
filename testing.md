# Testing the boxes

Once the software for the MCC DAQ hats has been installed, you can test the connections on the top of the box as follows.

## Verify Pi boots

1. Insert an SD card with the correct image into the Raspberry Pi.
2. Connect the HDMI, power, keyboard and mouse to the Raspberry Pi.
3. Power on.  Verify that the Pi boots.  Should take less than 30 seconds.
4. Verify that the keyboard and mouse works.
5. From the start menu, select `Accessories`, then open `MCC DAQ HAT Manager`.
6. Press the `List devices` button.  A dialog box should be shown that displays the following information:
   * 2 boards have been found.
   * Address 0 board is the MCC118 or MCC128 voltage input hat.
   * Address 1 board is the MCC134 thermocouple input hat.
7. Close the `List devices` dialog.
8. Open the MCC118 or MCC128 control app.  Press the `Open` button to
9. Apply a known voltage to the top BNC connector.  Verify that the expected voltage is shown on channel 0 of the app.
10. Repeat for the other BNC connector. Verify that the expected voltage is shown on channel 1 of the app.
11. Close app.
12. Open the MCC134 control app.  Select K type for channel 0 and channel 1.
13. Plug in K type thermocouple to top thermocouple socket. Verify that the expected temperature is shown on channel 0 of the app.
14. Plug in K type thermocouple to bottom thermocouple socket. Verify that the expected temperature is shown on channel 1 of the app.
15. Close app.

## Test rotary encoder inputs

If there is a 9 way DSUB female connector fitted to the box, perform the following tests.

1. Open a LXTerminal window.
2. Run the command `raspi-gpio get 4,22,23`.
3. Verify that all pins have `level=1`.
4. Insert jumper wire from pin 1 (ground) to pin 3.
5. Run the command `raspi-gpio get 4,22,23`.
6. Verify that GPIO4 and GPIO422 have `level=1`, and GPIO23 has `level=0`.
7. Insert jumper wire from pin 1 (ground) to pin 4.
8. Run the command `raspi-gpio get 4,22,23`.
9. Verify that GPIO22 and GPIO23 have `level=1`, and GPIO4 has `level=0`.
10. Insert jumper wire from pin 1 (ground) to pin 5.
11. Run the command `raspi-gpio get 4,22,23`.
12. Verify that GPIO4 and GPIO423 have `level=1`, and GPIO22 has `level=0`.

9 way DSUB connector pin number when viewed from outside of case.

Mappings of D-SUB pins to GPIO pins.

| DSUB Pin | Usage |
|---|---|
| 1 | Ground |
| 2 | 5V |
| 3 | GPIO23 |
| 4 | GPIO04 |
| 5 | GPIO22 |

```text
   -------------
   \ 5 4 3 2 1 /
    \ 9 8 7 6 /
     ---------
```
