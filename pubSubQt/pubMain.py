
import zmq
import random
import sys
import time
import cMsg


#Create a publisher socket
context = zmq.Context()
socket = context.socket(zmq.PUB) #Define publisher
socket.bind("tcp://*:5556") #Address as localhost 5555

##init communication class
cSocket = cMsg.csocket(socket)

#Label send data
topics = ["S1", "S2", "S3", "S4"]
startTime = time.perf_counter()
i = 0
#Loop publication
while True:
    topic = topics[i]
    messagedata = random.randrange(1, 215)
    cSocket.send(topic, messagedata, float(time.perf_counter() - startTime))
    time.sleep(0.001)
    i += 1
    if i ==3:
        i=0
    
    time.sleep(.001) #Sleep not to overheat CPU