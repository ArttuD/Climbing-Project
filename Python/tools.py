
import serial
import numpy as np

from PyQt6.QtCore import pyqtSignal,QThread

from queue import Queue

from filterpy.kalman import KalmanFilter

class sensorsampler(QThread):
    
    datapackage = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        
        self.com = None
        self.ser = None
        self.killCommand = Queue(maxsize=1)

    def initialize(self):
        """
        Initiliaze serial port connection
        """
        self.ser = serial.Serial(self.com, 9600, timeout=1000)
        self.ser.flush

    def start(self):
        """
        Start reading and unpacking until killcommand received
        Emit data to Qtplot
        """
        self.readData()

    def readData(self):
        while True:
            queueStatus = self.killCommand.empty()
            if queueStatus:
                line = self.ser.readline()
                parts = line.decode().strip().split('/')
                print(line)
                print(parts)

                if len(parts) == 7:
                    self.emitData(parts)
                else:
                    print('Ei hyvä pomo...')
            else:
                break

    def emitData(self,data):
        self.datapackage.emit(data)
    
    def closeSer(self):
        """
        Close the thing
        """
        self.ser.close()
        print('Closing')


class kalmanfilter():

    def __init__(self):
        self.f = KalmanFilter (dim_x=6, dim_z=3)
        self.dt = 1

        self.F = np.array([[1,self.dt,0.5*self.dt**2,0,0,0,0,0,0],
        [0,1,self.dt,0,0,0,0,0,0],
        [0,0,1,0,0,0,0,0,0],
        [0,0,0,1,self.dt,0.5*self.dt**2,0,0,0],
        [0,0,0,0,1,self.dt,0,0,0],
        [0,0,0,0,0,1,0,0,0],
        [0,0,0,0,0,0,1,self.dt,0.5*self.dt**2],
        [0,0,0,0,0,0,0,1,self.dt],
        [0,0,0,0,0,0,0,0,1]])

        self.f.F = self.F

        self.f.Q = np.eye(self.F.shape)*5e-3

        self.f.R = np.eye(3,3)*3e-1 #Check how this goes

    def predict(self):
        self.f.predict()

    def update(self,z):
        self.f.update(z)

    def returnEstimate(self):
        return self.f.x



