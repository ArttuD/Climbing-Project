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
