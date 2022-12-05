import serial
import cv2
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
# from PyQt5 import QtWidgets
import numpy as np
from matplotlib.widgets import Widget
import sys 
import zmq

class communicator:

    def __init__(self, com):
        self.com = com
        self.flag = True
        self.ser = None

    def initialize(self):
        self.ser = serial.Serial(self.com, 9600, timeout=1000)

    def readData(self):

        self.ser.flush

        while self.flag == True:
            line = self.ser.readline()
            parts = line.decode().strip().split('/')

            print(line)
            print(parts)

            if len(parts) == 7:
                self.flag=False
            else:
                print('Ei hyvä pomo...')
        
        self.flag=True
        return parts

         
    
    def closeSer(self):
        self.ser.close()
        print('Closing')

class serverCom:
    
    def __init__(self, name):
        self.portName = name
        self.context = None
        self.subscriber = None
        self.mgs = None

    def createConnections(self):
        context = zmq.Context()
        self.subscriber = context.socket(zmq.SUB)
        self.subscriber.connect(self.portName)
        self.subscriber.subscribe("") #sub all

    def collect(self):
        self.msg = self.subscriber.recv_multipart().split(",")
        return self.msg

    def kill(self):
        self.context.destroy()




class Visualizer:

    def __init__(self):

        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsView()
        self.win.setBackground('w')
        self.layout = pg.GraphicsLayout()
        self.win.setCentralItem(self.layout)

        self.acc_plot = self.layout.addPlot(0,0, title= 'Acceleration')

        self.acc_plot.setMouseEnabled(x=False,y=False)

        self.acc_plot.setLabel('left', 'Acceleration (m/s2)')

        self.acc_plot.setLabel('bottom', 't')

        self.acc = self.acc_plot.plot(pen='r')
        self.acc_y = self.acc_plot.plot(pen='b')
        self.acc_z = self.acc_plot.plot(pen='g')

        self.acc_buffer = np.zeros(100)
        self.acc_buffer_y = np.zeros(100)
        self.acc_buffer_z = np.zeros(100)

        self.acc_counter = np.zeros_like(self.acc_buffer)
        # self.color = pg.setConfigOption('background', 'w')
        self.win.show()

    def _check(self,x):
        if x is not None:
            return True
        else:
            return False

    # def _update_acc(self, acc_x, acc_y, acc_z, ts):
    #     if self._check(acc_x):
    #         self.acc_buffer = np.roll(self.acc_buffer, -1)
    #         self.acc_buffer[-1] = acc_x
    #         self.acc_counter = np.roll(self.acc_counter,-1)
    #         self.acc_counter[-1] = ts
            
    #         self.acc_buffer_y = np.roll(self.acc_buffer_y,-1)
    #         self.acc_buffer_y[-1] = acc_y

    #         self.acc_buffer_z = np.roll(self.acc_buffer_z,-1)
    #         self.acc_buffer_z[-1] = acc_z

    #         self.acc.setData(self.acc_counter,self.acc_buffer)
    #         self.acc_y.setData(self.acc_counter,self.acc_buffer_y)
    #         self.acc_z.setData(self.acc_counter,self.acc_buffer_z)

    #         # print(self.acc_buffer, self.acc_buffer_y, self.acc_buffer_z)

    def _update_acc(self,acc_x,acc_y,acc_z,ts):
        if self._check(acc_x):
            self.acc_buffer = np.roll(self.acc_buffer,-1)
            self.acc_buffer[-1] = acc_x
            self.acc_counter = np.roll(self.acc_counter,-1)
            self.acc_counter[-1] = ts
            
            self.acc_buffer_y = np.roll(self.acc_buffer_y,-1)
            self.acc_buffer_y[-1] = acc_y

            self.acc_buffer_z = np.roll(self.acc_buffer_z,-1)
            self.acc_buffer_z[-1] = acc_z

            self.acc.setData(self.acc_counter,self.acc_buffer)
            self.acc_y.setData(self.acc_counter,self.acc_buffer_y)
            self.acc_z.setData(self.acc_counter,self.acc_buffer_z)

    def update(self,acc_x=None,acc_y=None,acc_z=None,gyro_v=None,gyro_y=None,gyro_z=None,PID = None,ts=None):
        '''Update graph by giving acc, gyro and timestamp info as floats'''
        self._update_acc(acc_x,acc_y,acc_z,ts)  
          # print(acc_x, acc_y, acc_z)
        QtGui.QApplication.processEvents()

    def end(self):
        #pg.QtGui.QApplication.exec_()
        print("Closing visualizer")
        self.win.close()
        self.app.exit(0)

