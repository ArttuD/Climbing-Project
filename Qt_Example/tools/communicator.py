import string
from cv2 import exp
import serial
import numpy as np
import time
from mmap import ACCESS_DEFAULT
from multiprocessing import Queue
from sqlalchemy import true


class Communicator:

    def __init__(self):
        self.port = None
        self.bits = None
        self.path = None
        self.ser = None
        self.queue = Queue()

    def open_device(self,port, bits):
        self.port = port
        self.bits = bits
        self.ser = serial.Serial(port, bits, timeout = 1)


    def read(self):
        val = self.ser.readline().decode().strip()
        self.queue.put(val)

    def parse(self):
        if not self.queue.empty():
            package = self.queue.get(block=False)
            counts = package.count('/')
            # too short skip
            if counts != 7:
                if not self.queue.empty():
                    package2 = self.queue.get(block=False)
                    return package2,True
                else:
                    return None,False
            else:
                return package,True
        return None,False


    def unstack(self,val):
        data_row = val.split("/")
        Acc = [float(x) for x in data_row[:3]]
        Gy = [float(x) for x in data_row[3:6]]
        PID = float(data_row[6])
        timestep = float(data_row[-1][:-1])
        return Acc,Gy,PID,timestep,True



    def read_device(self):
        #time.sleep(0.001)       
        val = self.ser.readline()
        #while not '\\n' in str(val):
        #    #time.sleep(0.01)
        #    line = self.ser.readline()
        #    if not not line.decode():
        #        val = (val.decode() + line.decode()).encode()
        try:
            val = val.decode()
        except UnicodeDecodeError:
            return None,None,None,None,False
        val = val.strip()
        if val.count('/') != 7:
            return None,None,None,None,False
        else:
            data_row = val.split("/")
            Acc = [float(x) for x in data_row[:3]]
            Gy = [float(x) for x in data_row[3:6]]
            PID = float(data_row[6])
            timestep = float(data_row[-1][:-1])
            return Acc,Gy,PID,timestep,True

    def end(self):
        print("closing device")
        self.ser.close()

    def write_device(self,x):
        for i in range(5):
            self.ser.write(x.encode())
        time.sleep(0.01)
        started = False
        while True:
            val = self.ser.readline()
            #while not '\\n' in str(val):
            #    time.sleep(0.01)
            #    line = self.ser.readline()
            #    if not not line.decode():
            #        val = (val.decode() + line.decode()).encode()
            val = val.decode()
            val = val.strip()
            if val != "0":
                time.sleep(0.1)
                break
            else:
                self.ser.write(x.encode())
                time.sleep(0.01)
        
        time.sleep(0.05)
