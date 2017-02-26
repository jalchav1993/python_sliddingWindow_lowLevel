#! /bin/python
import sys, re  
from socket import *
import json
# default params
serverAddr = ('localhost', 50001)       

#file location
fileLoc = '~/'

print("sending")
s_1 = {'request':'get', 'params':'file1'}
s_2 = json.dumps(s_1)
n = 0
state = 0
while 1:
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.settimeout(5)
    clientSocket.sendto(s_2, serverAddr)
    response, serverAddrPort = clientSocket.recvfrom(2048)
    if response:
        s_1 = {'request':'ack', 'params':n}
        s_2 = json.dumps(s_1)
        n += 1
        
    clientSocket.close()
    print(response)