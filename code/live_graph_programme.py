#Importing data packs
import sys
from daqhats import hat_list, HatIDs, mcc118
import time
import numpy as np
import threading
import math
from datetime import datetime
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#Initialise variables

plot_friction = []
plot_time = []
gFile = None

class DataReader(threading.Thread):
    def __init__(self):
        
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        
        self.board = None
        self.board_list = hat_list(filter_by_id = HatIDs.ANY)
        if not self.board_list:
            print ("No boards found")
            sys.exit()
        else:
            for entry in self.board_list:
                if entry.id == HatIDs.MCC_118:
                    self.board = mcc118(entry.address)
                    break 
    def stop(self):
        print("Called stop")
        self._stop_event.set()

    def is_stopped(self):
        return self._stop_event.is_set()
    
    def readvalue(self):
        value = (-1 * self.board.a_in_read(0)) #Reading the channel connected to the pendulum tribometer
        return value
    
    def convertdata(self,value):
        voltage = value + 0.3 #Value taken from the difference at 0
        angle_DEG = (voltage)*9.5 #Calibration value taken experimentally from the pendulum
        angle_RAD = (angle_DEG*3.14159265)/180
        c_o_f =(abs(math.sin(angle_RAD))/(math.tan(1.0472))) #Processing angle data to Friction data
        return (voltage, angle_DEG, c_o_f)

    def append2plot(self, now,c_o_f):
        global plot_time, plot_friction
        plot_time.append(now.timestamp())
        plot_friction.append(c_o_f)
        
 
    def run(self):
        global plt
        try:
            while True:
                raw_value = self.readvalue()
                data = self.convertdata(raw_value)
                voltage = data[0]
                angle_DEG = data[1]
                c_o_f = data[2]
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print ("{}: Ch {}: {:.3f}: Angle {}".format(current_time, 0, raw_value, angle_DEG))#Prints the raw data value
                writefiledata(current_time, voltage, angle_DEG, c_o_f) #Writes file data
                self.append2plot(now, c_o_f)
                #Need to break loop to close file
                time.sleep(0.2)
        except KeyboardInterrupt:
            pass
        print("Thread stopped")
        plt.close("all")


    #Opening .txt file for writing
def openfile():
    """ Open file to store results."""
    global gFile
    gFile = open("nogreasetest41rpm.txt","a")
    
    
def openplotwindow():
    #Initialise plot style
    global plt
    plt.style.use('fivethirtyeight')

#Writing data function
def writefiledata(t,v,a,f):
    global gFile
    time = t
    voltage = str(round(v, 3))
    angle = str(round(a,2))
    friction = str(round(f,3))
    gFile.write(time +"\t"+ voltage +"\t"+ angle +"\t"+ friction)
    gFile.write("\n")
    

#Defining animate function for graph which reads, processes and saves the data
def animate(i):
    global plot_time, plot_friction
    plt.cla() 
    plt.plot(plot_time, plot_friction)
    plt.title("Friction Coefficient Against Time")
    plt.xlabel("Time [seconds]")
    plt.ylabel("Friction coefficient")

    
def setup():
    openfile()
    openplotwindow()
    
def closefile():
    print("Closing file")
    global gFile
    gFile.flush()
    gFile.close()
    
def main():
    setup()
    print("Starting thread...")
    reader = DataReader()
    reader.start()
    print("Starting plot...")
    ani = FuncAnimation(plt.gcf(), animate, interval = 10) #Animating the graph to update for every new data set
    plt.tight_layout()
    # plt.show never ends unless plt.close is used.
    plt.show()
    closefile()

main()

    #tidyup()
    
