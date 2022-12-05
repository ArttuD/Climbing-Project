from tools import communicator, Visualizer
import cv2
import numpy as np
import os

com = communicator('COM7')
vis = Visualizer()
com.initialize()

flag=0

try:
    datas = []
    while True:
        
        data = list(map(float,com.readData()))
        datas.append(data)
        flag+=1
        print(data)
        # Acc,Gy,PID,timestep,ret = com.unstack(data)
        vis.update(data[0],data[1],data[2],data[3],data[4],data[5],ts=data[6])

except KeyboardInterrupt:
    
    i = 0
    while True:
        i+=1
        if not os.path.exists('data' + str(i) + '.txt'):
            np.savetxt('data' + str(i) + '.txt' ,datas, fmt=f'%.4e')
            break

com.closeSer()
vis.end()
