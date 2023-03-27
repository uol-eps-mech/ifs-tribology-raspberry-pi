# Example from:
# https://thingsdaq.org/2022/03/09/encoder-with-raspberry-pi/

import time
import numpy as np
from gpiozero import RotaryEncoder

#Assigning parameter values
ppr = 1200 #Pulse per revolution
tstop = 30 #Loop execution duration (s)
tsample = 0.02 #Sampling period for code execution (s)
tdisp = 0.5 #Sampling period for values display

#Creating encoder object using GPIO pins
encoder = RotaryEncoder(23, 4, max_steps=0)

#Intializing values and starting the clock
anglecurr = 0
tprev = 0
tcurr = 0
tstart = time.perf_counter()

#Loop that displays the current angular position of the encoder shaft
print ('Running code for', tstop, 'seconds...')
print ('Turn encoder')
while tcurr <= tstop:
    #Giving time
    time.sleep(tsample)
    #Getting time
    tcurr = time.perf_counter() - tstart
    #Getting angular position of encoder
    anglecurr = 360 / ppr * encoder.steps
    #Printing angular position
    if (np.floor(tcurr/tdisp) - np.floor(tprev/tdisp)) == 1:
        print("Angle = {:0.0f} deg" .format(anglecurr))
        print("Time = {:0.0f} seconds" .format(tcurr))

    #Update old values
    tprev = tcurr

print('Done.')
#Releasing GPIO pins
encoder.close()