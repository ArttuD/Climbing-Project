import pyqtgraph as pg
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import time

class Visualizer():

    def __init__(self):
        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsView()
        self.layout = pg.GraphicsLayout()
        self.win.setCentralItem(self.layout)
        self.win.show()
        self.Acc_plot = self.layout.addPlot(0,0,title = "Acceleration")
        self.Gy_plot = self.layout.addPlot(1,0,title = "Gyroscope")

        self.Acc_plot.setMouseEnabled(x = False, y= False)
        self.Gy_plot.setMouseEnabled(x = False, y= False)

        self.Acc_plot.setLabel('left', "m/s")
        self.Gy_plot.setLabel('left', "rad/s")    
        self.Acc_plot.setLabel('bottom', "t")
        self.Gy_plot.setLabel('bottom', "t")

        self.Acc_x = self.Acc_plot.plot(pen="r")
        self.Gy_x = self.Gy_plot.plot(pen="b")

        self.Acc_buffer = np.zeros(100)
        self.Acc_buffer_y = np.zeros(100)
        self.Gy_buffer = np.zeros(100)

        self.Acc_counter = np.zeros_like(self.Acc_buffer)
        self.Gy_counter = np.zeros_like(self.Gy_buffer)

        #self.app.aboutToQuitconnect(self.end)

    def _check(self,x):
        if x is None:
            return True
        else:
            return False

    def _update_Acc(self,Acc_d_x,Acc_d_y,ts):
        if self._check(Acc_d_x):
            self.Acc_buffer = np.roll(self.Acc_buffer, -1)
            self.Acc_buffer[-1] = Acc_d_x
            self.Acc_counter = np.roll(self.Acc_counter, -1)
            self.Acc_counter[-1] = ts
            #y
            self.Acc_buffer_y = np.roll(self.Acc_y_buffer, -1)
            self.Acc_buffer_y[-1] = Acc_d_y


            self.Gy_x.SetData(self.Acc_counter,self.Acc_buffer)
            self.Gy_x.SetData(self.Acc_counter,self.Acc_buffer_y)


    def _update_Gy(self,Gy_d,ts):
        if self._check(Gy_d):
            self.Gy_buffer = np.roll(self.Gy_buffer, -1)
            self.Gy_buffer[-1] = Gy_d
            self.Gy_counter = np.roll(self.Gy_counter, -1)
            self.Gy_counter[-1] = ts

            self.Gy.SetData(self.Gy_counter,self.Gy_buffer)

    def update(self,Acc_d_x = None,Acc_d_y = None, Gy_d = None, ts = None):
        self._update_Acc(Acc_d_x,Acc_d_y,ts)
        self._update_Gy(Gy_d,ts)

        QtGui.QApplication.processEvents()

    def end(self):
        #pg.QtGui.QApplication.exec_()
        print("closing visualizer")
        self.win.close()
        self.app.exit(0)
    
if __name__ == "__main__":
    vis = Visualizer()
    n = 60 
    Acc= np.random.normal(0,1,n)
    Gy= np.random.normal(0,1,n)
    times= np.linspace(0,150,n)
    for ts,h,t in zip(times,Acc,Gy):
        vis.update(h,t,ts)
        time.sleep(0.1)
    vis.end()
