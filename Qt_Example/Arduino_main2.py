import numpy as np
from tools.pq import Visualizer
from tools.communicator import Communicator 
import signal
import sys

#Vizualizes
vis = Visualizer()
#Communicate with serial port
com = Communicator()


com.open_device("com4", 19200)
#com.write_device("1")

def handler(signum,frame):
    com.write_device("0")
    com.end()
    vis.end()
    sys.exit("quiting")

i = 0
signal.signal(signal.SIGINT,handler)
com.ser.reset_input_buffer()
com.ser.reset_output_buffer()
com.write_device("1")

while i < 1000:
    read = com.read()
    ret,cond = com.parse()
    if cond:
        print(ret)
        Acc,Gy,PID,timestep,ret = com.unstack(ret)
        vis.update(Acc[0],Acc[1],Acc[2],Gy[0],Gy[1],Gy[2],PID,timestep)
    else:
        print("ei ketään missään")
    i += 1

com.write_device("0")
com.end()
vis.end()