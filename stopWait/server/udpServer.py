#! /bin/python
from socket import *
import sys
import json

def fileExists(params):
    return params == fileName
    
_S_INIT = 's_init'
_S_SEND = 's_send'
_S_WAIT = 's_wait'

state = _S_INIT
ackCount = 0;

fileName = "file1"
fileCont = {0:'0_o', 1:'1_o', 2:'2_o'}

# default params
serverAddr = ("", 50001)

print "binding datagram socket to %s" % repr(serverAddr)

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(serverAddr)

print "ready to receive"

while 1:
    message, clientAddrPort = serverSocket.recvfrom(2048)
    print "from %s: rec'd '%s'" % (repr(clientAddrPort), message)
    data = json.loads(message)
    request = data['request']
    params = data['params']
    
    if state == _S_INIT:
        if request == "get" and fileExists(params):
            serverSocket.sendto(fileCont[ackCount], clientAddrPort)
            state = _S_WAIT
        elif request == "get" and not fileExists(params):
            serverSocket.sendto("404", clientAddrPort)
            state = _S_INIT
        
    elif state == _S_WAIT:  
        if request == "ack":
            if params == ackCount:
                ackCount += 1
                if ackCount not in fileCont:
                    serverSocket.sendto("close", clientAddrPort)
                    state = _S_INIT
                    ackCount = 0
                else:
                    serverSocket.sendto(fileCont[ackCount], clientAddrPort)
                    state = _S_WAIT
                    
            elif params < ackCount and params >= 0:
                serverSocket.sendto(fileCont[params], clientAddrPort)
                state = _S_WAIT
                
        elif request == "get":
            # Case where the server answer for data[0] was lost after client started get
            if fileExists(params):
                serverSocket.sendto(fileCont[0], clientAddrPort)
                state = _S_WAIT
            elif not fileExists(params):
                serverSocket.sendto("404", clientAddrPort)
                state = _S_INIT
                
    print(state);
    
