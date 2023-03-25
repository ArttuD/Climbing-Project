
import numpy as np
import sys


from PyQt6.QtWidgets import QWidget,QGridLayout,QVBoxLayout,QPushButton
from PyQt6.QtCore import pyqtSlot
from PyQt6 import QtWidgets
import pyqtgraph as pg
#import pyqtgraph.opengl as gl
import time
from tools import sensorsampler


class App(QWidget):
    
    def __init__(self):
        super().__init__()


        self.win = QWidget()
        self.initGUI()

        self.sensor = sensorsampler()
        self.sensor.datapackage.connect(self.receiveData)

    def initGUI(self):
        
        self.layout = QGridLayout()
        
        self.initLayouts()
        self.initButtons()
        self.initGraphs()
        
        self.win.setLayout(self.layout)
        

        self.win.show()

    def initLayouts(self):
        self.layout = QGridLayout()
        self.Vlayout = QVBoxLayout()

    def initButtons(self):

        self.startbtn = QPushButton("start")
        self.startbtn.pressed.connect(self.start)
        self.startbtn.setStyleSheet("background-color : green")
        self.layout.addWidget(self.startbtn,0, 0)

        self.stopbtn = QPushButton("stop")
        self.stopbtn.pressed.connect(self.stop)
        self.stopbtn.setStyleSheet("background-color : red")
        self.Vlayout.addWidget(self.stopbtn)

        self.shutbtn = QPushButton("Shutdown")
        self.shutbtn.pressed.connect(self.shutdown)
        self.shutbtn.setStyleSheet("background-color : red")
        self.Vlayout.addWidget(self.shutbtn)

        self.layout.addLayout(self.Vlayout,0,1)

    def start(self):
        pass

    def stop(self):
        pass

    def shutdown(self):
        self.close()
        print("Shutting down")
        exit(0)

    def initGraphs(self):
        #self.create3Dplot()
        self.create2Dplots()
        pass

    def initData(self):

        self.time = np.empty(100)

        self.AccX = np.empty(100)
        self.AccY = np.empty(100)
        self.AccZ = np.empty(100)

        self.RotX = np.empty(100)
        self.RotY = np.empty(100)
        self.RotZ = np.empty(100)



    def create2Dplots(self):
        self.initData()

        self.GyroA = pg.PlotWidget()
        self.GyroA.setTitle("Acceleration", color = "r")
        self.GyroA.setLabel("left", "Acceleration (m/s^2)")
        self.GyroA.setLabel("bottom", "Time (s)")
        self.GyroA.addLegend()
        
        #Set Range
        self.GyroA.setXRange(0, 10, padding=0)
        self.GyroA.setYRange(0, 10, padding=0)

        self.GyroAXCurve = self.GyroA.plot(self.time, self.AccX, name="Acc - X",  pen=pg.mkPen(color=(255, 0, 0)), symbol='+', symbolSize=10, symbolBrush=('b'))
        self.GyroAYCurve = self.GyroA.plot(self.time, self.AccY, name="Acc - Y",  pen=pg.mkPen(color=(0, 255, 0)), symbol='o', symbolSize=10, symbolBrush=('b'))
        self.GyroAZCurve = self.GyroA.plot(self.time, self.AccZ, name="Acc - Z",  pen=pg.mkPen(color=(0, 0, 255)), symbol='s', symbolSize=10, symbolBrush=('b'))

        self.layout.addWidget(self.GyroA,1,0)
        
        self.GyroR = pg.PlotWidget()
        self.GyroR.setTitle("Rotation", color = "r")
        self.GyroR.setLabel("left", "Rotation (rad)")
        self.GyroR.setLabel("bottom", "Time (s)")
        self.GyroR.addLegend()
        
        #Set Range
        self.GyroR.setXRange(-10, 10, padding=0)
        self.GyroR.setYRange(-10, 10, padding=0)

        self.GyroRXCurve = self.GyroR.plot(self.time, self.RotX, name="Rot - X",  pen=pg.mkPen(color=(255, 0, 0)), symbol='+', symbolSize=10, symbolBrush=('b'))
        self.GyroRYCurve = self.GyroR.plot(self.time, self.RotY, name="Rot - Y",  pen=pg.mkPen(color=(0, 255, 0)), symbol='o', symbolSize=10, symbolBrush=('b'))
        self.GyroRZCurve = self.GyroR.plot(self.time, self.RotZ, name="Rot - Z",  pen=pg.mkPen(color=(0, 0, 255)), symbol='s', symbolSize=10, symbolBrush=('b'))

        self.layout.addWidget(self.GyroR,1,1)


    def create3Dplot(self):

        # create the background grids
        self.Gw = gl.GLViewWidget()
        gx = gl.GLGridItem()
        gx.rotate(90, 0, 1, 0)
        gx.translate(-10, 0, 0)
        self.GLw.addItem(gx)
        gy = gl.GLGridItem()
        gy.rotate(90, 1, 0, 0)
        gy.translate(0, -10, 0)
        self.GLw.addItem(gy)
        gz = gl.GLGridItem()
        gz.translate(0, 0, -10)
        self.GLw.addItem(gz)

    @pyqtSlot(object)
    def receiveData(self,data):
        """
        Signal pipe
        """
        self.time = np.roll(self.time,-1); self.time[-1] = data[0]

        self.AccX = np.roll(self.AccX,-1); self.AccX[-1] = data[1]
        self.AccY = np.roll(self.AccY,-1); self.AccY[-1] = data[2]
        self.AccZ = np.roll(self.AccZ,-1); self.AccZ[-1] = data[3]

        self.GyroAXCurve.setData(self.time, self.AccX)
        self.GyroAYCurve.setData(self.time, self.AccY)
        self.GyroAZCurve.setData(self.time, self.AccZ)

        self.RotX = np.roll(self.RotX,-1); self.RotX[-1] = data[4]
        self.RotY = np.roll(self.RotY,-1); self.RotY[-1] = data[5]
        self.RotZ = np.roll(self.RotZ,-1); self.RotZ[-1] = data[6]

        self.GyroRXCurve.setData(self.time, self.RotX)
        self.GyroRYCurve.setData(self.time, self.RotY)
        self.GyroRZCurve.setData(self.time, self.RotZ)

def pymain():
    app = QtWidgets.QApplication(sys.argv)
    time.sleep(1)
    w = App()
    sys.exit(app.exec())

if __name__ == "__main__":
    pymain()