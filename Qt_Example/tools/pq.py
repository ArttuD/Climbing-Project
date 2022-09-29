from matplotlib.widgets import Widget
import pyqtgraph as pg
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore 
import time


class Visualizer:
    '''Visualize acc and gyro data
    Usage: vis = Visualizer()
            while True:
                vis.update(current_acc,current_gyro_v,timestamp)
            vis.end()
    '''
    def __init__(self):
        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsView()
        self.layout = pg.GraphicsLayout()
        self.win.setCentralItem(self.layout)
        self.acc_plot = self.layout.addPlot(0,0,title="Acceleration")
        self.gyro_plot = self.layout.addPlot(1,0,title="Rotation")
        self.PID_plot = self.layout.addPlot(2,0,title="Feedback")

        self.acc_plot.setMouseEnabled(x=False,y=False)
        self.gyro_plot.setMouseEnabled(x=False,y=False)
        self.PID_plot.setMouseEnabled(x=False,y=False)

        self.acc_plot.setLabel('left', "Acceleration (m/s2)")
        self.gyro_plot.setLabel('left', "Rotation")
        self.PID_plot.setLabel('left', "Control value")
        
        self.acc_plot.setLabel('bottom', "t") 
        self.gyro_plot.setLabel('bottom', "t") 
        self.PID_plot.setLabel('bottom', "t") 

        self.acc = self.acc_plot.plot(pen='r')
        self.acc_y = self.acc_plot.plot(pen='b')
        self.acc_z = self.acc_plot.plot(pen='g')
        self.gyro = self.gyro_plot.plot(pen='r')
        self.gyro_y = self.gyro_plot.plot(pen='b')
        self.gyro_z = self.gyro_plot.plot(pen='g')

        self.PID = self.PID_plot.plot(pen='r')

        self.acc_buffer = np.zeros(100)
        self.acc_buffer_y = np.zeros(100)
        self.acc_buffer_z = np.zeros(100)

        self.gyro_buffer = np.zeros(100)
        self.gyro_buffer_y = np.zeros(100)
        self.gyro_buffer_z = np.zeros(100)

        self.PID_buffer = np.zeros(100)

        self.acc_counter = np.zeros_like(self.acc_buffer)
        self.gyro_counter = np.zeros_like(self.gyro_buffer)

        self.PID_counter = np.zeros_like(self.PID_buffer)

        #buttons
        #b1 = QPushButton(Widget)
        #b1.setText("Stop")
        #b1.clicked.connect(self.on_b1_clicked)

        ##create buttoms
        self.win.show()


    #def connections(self):
    #    self.b1.clicked.connect(self.on_b1_clicked)
    #    self.b2.clicked.connect(self.on_b2_clicked)
    #    #self.app.aboutToQuit.connect(self.end)

    #def on_b1_clicked(self):
    #    #Stop the system
    #    print("stopping")
    #    self.end()

    # def on_b2_clicked(self):
        #read  field        

    def _check(self,x):
        if x is not None:
            return True
        else:
            return False

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

    def _update_gyro(self,gyro_v,gyro_y,gyro_z,ts):
        if self._check(gyro_v):
            self.gyro_buffer = np.roll(self.gyro_buffer,-1)
            self.gyro_buffer[-1] = gyro_v
            self.gyro_counter = np.roll(self.gyro_counter,-1)
            self.gyro_counter[-1] = ts

            self.gyro_buffer_y = np.roll(self.gyro_buffer_y,-1)
            self.gyro_buffer_y[-1] = gyro_y

            self.gyro_buffer_z = np.roll(self.gyro_buffer_z,-1)
            self.gyro_buffer_z[-1] = gyro_z

            self.gyro.setData(self.gyro_counter,self.gyro_buffer)
            self.gyro_y.setData(self.acc_counter,self.gyro_buffer_y)
            self.gyro_z.setData(self.acc_counter,self.gyro_buffer_z)

    def _update_PID(self,PID,ts):
        if self._check(PID):
            self.PID_buffer = np.roll(self.PID_buffer,-1)
            self.PID_buffer[-1] = PID
            self.PID_counter = np.roll(self.PID_counter,-1)
            self.PID_counter[-1] = ts

            self.PID.setData(self.PID_counter,self.PID_buffer)


    def update(self,acc_x=None,acc_y=None,acc_z=None,gyro_v=None,gyro_y=None,gyro_z=None,PID = None,ts=None):
        '''Update graph by giving acc, gyro and timestamp info as floats'''
        self._update_acc(acc_x,acc_y,acc_z,ts)
        self._update_gyro(gyro_v,gyro_y,gyro_z,ts)
        self._update_PID(PID,ts)

        QtGui.QApplication.processEvents()

    def end(self):
        #pg.QtGui.QApplication.exec_()
        print("Closing visualizer")
        self.win.close()
        self.app.exit(0)

if __name__ == "__main__":
    # Demo with random data
    vis = Visualizer()
    n = 60
    acc_v = np.random.normal(0,1,n)
    gyro_v = np.random.normal(0,1,n)
    times = np.linspace(0,150,n)

    for ts,h,t in zip(times,acc_v,gyro_v):
        vis.update(h,t,ts)
        time.sleep(0.1)
    # remember to stop
    vis.end()

