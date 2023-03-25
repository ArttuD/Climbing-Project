from tools import communicator
import cv2
import numpy as np
import os
import pyQt6

#com = communicator('COM7')
vis = Visualizer()
server = serverCom("tcp://localhost:5556")
#com.initialize()
server.createConnections()
flag=0

try:
    datas = []
    while True:
        
        #data = list(map(float,com.readData()))
        #datas.append(data)
        flag+=1
        data = server.collect()
        vis.update(data[0],data[1],data[2],data[3],data[4],data[5],ts=data[6])

except KeyboardInterrupt:
    
    i = 0
    while True:
        i+=1
        if not os.path.exists('data' + str(i) + '.txt'):
            np.savetxt('data' + str(i) + '.txt' ,datas, fmt=f'%.4e')
            break

#com.closeSer()
server.kill()
vis.end()
