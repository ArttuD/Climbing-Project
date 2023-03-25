#https://www.pythonguis.com/tutorials/plotting-matplotlib/
#https://github.com/Sensirion/libsensors-python/blob/master/streaming_plot_client.py
#Datalocker: https://doc.qt.io/qtforpython/tutorials/datavisualize/plot_datapoints.html
#https://github.com/JustinTulloss/zeromq.node/blob/master/examples/pub_sub.js
"""
import sys
import zmq
import cMsg

#Create a socket to listen local server

context = zmq.Context()
socket = context.socket(zmq.SUB)
cSocket = cMsg.csocket(socket)

socket.connect("tcp://localhost:5556")

#Sub only defined topics 
topicfilter = ["S1", "S2", "S3", "S4"]
for i in topicfilter:
    socket.subscribe(i)
i=0
while i<10000:
    print("Waiting data")
    topic, message = cSocket.recv()
    print("topic: ", topic, " message: ", message)
    i += 1
"""
import sys
import zmq
from PyQt5 import QtGui,QtWidgets
import cMsg
import pyqtgraph as pg

app = pg.QtGui.QApplication(sys.argv)

mw = cMsg.QtWindow()
pg.QtGui.QApplication.processEvents()
sys.exit(app.exec_())


"""
Classes from tools

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


"""