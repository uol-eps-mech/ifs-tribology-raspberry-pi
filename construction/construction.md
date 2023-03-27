# Construction

## BOM

TODO Finish this off.

Per unit

* 1 x 3D printed case.
* 2 x BNC sockets, chassis mount.
* 2 x K type thermocouple sockets. https://uk.rs-online.com/web/p/sensor-accessories/4559742
* 1 x Adafruit Perma-Proto board ADA2310 - https://shop.pimoroni.com/products/adafruit-perma-proto-hat-for-pi-mini-kit?variant=1038451613

Optional

1 x 9 way DSUB female chassis mount.  https://uk.rs-online.com/web/p/d-sub-connectors/7873852

Additional parts

1 box - https://www.amazon.co.uk/GeeekPi-Standoffs-Assortment-Box%EF%BC%8CMale-Female-Screwdriver/dp/B07PHBTTGV
1 pack  4 fans and heat sinks.

## Wiring of rotary encoder

There are three GPIO pins that are used to monitor the rotary encoder output.  The outputs are:

A - Rotary encoder position A
B - Rotary encoder position B
Z - Rotary encoder index (one pulse per revolution).

We only need RPM so just use the Z output.

