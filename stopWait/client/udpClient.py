#! /bin/python
import sys, re  
from socket import *
import json

#prototypes and functions
def buildRequest(requset, param):
    return json.dumps({'request':requset, 'params':param})

_C_INIT = "c_initial"       # state definition: initial
_C_WAIT = "c_waiting"       # state definition: waiting for data
_C_ACK = "c_acking"  # state definition: accepting data
# default params
serverAddr = ('localhost', 50000)

state = _C_INIT             # current state
ackCount = 0                # count of successful transmit
timeout = .025                 # timeout for socket thread
fileName = 'file1'          # file location
packegeDropCount = 0

while 1:
    print("sending")
    print ("state: %s" % state)
    print ("ack[%s]" % ackCount)
    if state == _C_INIT:
        message = buildRequest("get", fileName)
    elif state == _C_WAIT or state == _C_ACK:
        message = buildRequest("ack", ackCount)
        
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.settimeout(timeout)
    response = ''
    serverAddrPort =''
    try:
        clientSocket.sendto(message, serverAddr)
        response, serverAddrPort = clientSocket.recvfrom(2048)
    except:
        print("519 timedout, trying again")
        if state != _C_INIT:
            state = _C_WAIT
        packegeDropCount += .005
        timeout +=  packegeDropCount
    else:
        if response == "close":
            print("file transmission is over")
            break;
        elif response == "404":
            print ("404, unknown file")
            state = _C_INIT
        elif state == _C_WAIT or state == _C_INIT:
            state = _C_ACK
        elif state == _C_ACK:
            ackCount += 1
            state = _C_ACK
        print(response)
        clientSocket.close()
    
        
       
       
    