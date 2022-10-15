import re
import json

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
            self.pakcer = packer

    def dumps(self, name, data):
        #Encode for sending
        return b'\x00'.join((name.encode(), self.packer.dumps(data)))

    def loads(self, data):
        name, data = UNPACK(data).groups()
        return name.decode(), self.packer.loads(data)

class csocket(Packer):
    
    def __init__(self,socket, packer = None):
            self.socket = socket
            super().__init__(packer)

    def send(self, name, data):
        self.socket.send(self.dumps(str(name), data))
        print("Sending: ", self.dumps(str(name), data))

    def recv(self):
        return self.loads(self.socket.recv())
