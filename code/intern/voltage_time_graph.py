#Importing data packs
import sys
from daqhats import hat_list, HatIDs, mcc118
import time
import numpy as np
import matplotlib.pyplot as plt

#Gets hat list of the Daqhat Boards
board_list = hat_list(filter_by_id = HatIDs.ANY)
if not board_list:
    print ("No boards found")
    sys.exit()
 
#Initialise logging
 
n=1 # Channel Number
Tstop = 20 #Logging time (Seconds)
Ts = 1 # Sampling time (Seconds)
N= int(Tstop/Ts)#Loop iteration
data = []


#Open file for data
file = open("test003.txt","w")

#Write to text file function
def writefiledata(t, v):
    time = str(t)
    value = str(round(v, 3))
    file.write(time + "\t" + value)
    file.write("\n")
#Reads and displays values for Channel 0 and 1 in a loop
for k in range(N):
    for entry in board_list:
        if entry.id == HatIDs.MCC_118:
            board = mcc118(entry.address)
            value = (-1*board.a_in_read(1))
            print ("Ch {0}: {1:.3f}".format(1, value))
            data.append(value)
    time.sleep(Ts)
    writefiledata(k*Ts, value)
    
#File close
file.close()

#Plotting
t=np.arange(0,Tstop,Ts)
plt.plot(t,data,"-o")
plt.title("Voltage against Time")
plt.xlabel("Time [seconds}")
plt.ylabel("Voltage [v]")
plt.grid()
Vmin = -5; Vmax =5
plt.axis([0,Tstop,Vmin,Vmax])
plt.show()