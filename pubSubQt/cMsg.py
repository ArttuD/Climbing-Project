import re
import json

import zmq
from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import numpy as np

try:
    import msgpack
    MPACK = True
except ImportError:
    MPACK = False

UNPACK = re.compile(b'(.*)\x00(.*)').match

class Packer:
    #helper class for zeroMQ communicator
    def __init__(self,packer = None):
        #If MPack installed use it otherwise json or externally defined
        if packer is None:
            self.packer = msgpack if MPACK else json
        else:
            self.packer = packer

    def dumps(self, name, data):
        #Encode for sending
        return b'\x00'.join((name.encode(), self.packer.dumps(data)))

    def loads(self, data):
        try:
            name, data = UNPACK(data).groups()
            return name.decode(), self.packer.loads(data)
        except:
            return "S1", 0

class csocket(Packer):
    
    def __init__(self,socket, packer = None):
            self.socket = socket
            super().__init__(packer)

    def send(self, name, data):
        self.socket.send(self.dumps(str(name), data))
        print("Sending: ", self.dumps(str(name), data))

    def recv(self):
        return self.loads(self.socket.recv())


class subcriber(QtCore.QObject,Packer):

    message = QtCore.pyqtSignal(float)

    def __init__(self, packer = None):
        QtCore.QObject.__init__(self)
        super().__init__(packer)
        #Socket to sub the local server
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect("tcp://localhost:5556")

        #Listen only certain topics
        filterTopics = ["S1","S2","S3","S4"]
        for i in filterTopics:
            #self.socket.setsockopt(zmq.SUBSCRIBE, i)
            self.socket.subscribe(i)

        self.running = True

    def loop(self):
        while self.running:
            string = self.socket.recv()
            name, data = UNPACK(string).groups()
            print(name.decode())
            print(self.packer.loads(data))
            self.message.emit(float(self.packer.loads(data)))


class QtWindow(QtWidgets.QMainWindow):

    def __init__(self,parent = None):
        QtWidgets.QMainWindow.__init__(self, parent)
        """
        frame = QtWidgets.QFrame()
        label = QtWidgets.QLabel("listening")
        self.textEdit = QtWidgets.QTextEdit()

        layout = QtWidgets.QVBoxLayout(frame)
        layout.addWidget(label)
        layout.addWidget(self.textEdit)

        self.setCentralWidget(frame)
        """
        self.step = 0
        #Create window and set the layout
        self.win = pg.GraphicsView()
        self.layout = pg.GraphicsLayout()
        self.win.setCentralItem(self.layout)
        self.Accplot = self.layout.addPlot(0,0,title = "Acceleration")
        
        #Modify and tune subplots
        self.Accplot.setMouseEnabled(x = False, y= False)
        self.Accplot.setLabel("left", r"a [$\frac{m}{s^2}$]")
        self.Accplot.setLabel("bottom", "time [s]")
        self.Acc = self.Accplot.plot(pen = "r")

        #Init data
        self.AccBuffer = np.zeros(100)
        self.AccCounter = np.zeros_like(self.AccBuffer)

        self.thread = QtCore.QThread()
        self.zeromqListener = subcriber()
        self.zeromqListener.moveToThread(self.thread)

        self.thread.started.connect(self.zeromqListener.loop) 
        self.zeromqListener.message.connect(self.signalReceiver)       

        QtCore.QTimer.singleShot(0, self.thread.start)
        self.win.show()

    def signalReceiver(self, message):
        #self.textEdit.append("%s\n" %message)
        self.AccBuffer = np.roll(self.AccBuffer,-1)
        self.AccBuffer[-1] = float(message)

        self.AccCounter = np.roll(self.AccCounter,-1)
        self.AccCounter[-1] = self.step
        self.step = self.step + 1
        self.Acc.setData(self.AccCounter,self.AccBuffer)

    def closeEvent(self,event):
        self.zeromqListener.running = False
        self.thread.quit()
        self.thread.wait()

    def _check(self,x):
        if x is not None:
            return True
        else:
            return False
