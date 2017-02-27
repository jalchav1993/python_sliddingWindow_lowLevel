#! /bin/python
from socket import *
import sys
import json
    
_S_INIT = 's_init'
_S_SEND = 's_send'
_S_WAIT = 's_wait'

state = _S_INIT
ackCount = 0;

fileBuffer = []
fileSize = 0
step = 0
fileSize = 0

def fileExists(params):
    try:
       file_dl = open(params, 'r') #for size
       fileSize = len(file_dl.read())
       file_dl.close()
       file_dl = open(params, 'r') #for lines
       window = 10
       if fileSize > 1000:
           window = 100
       elif fileSize >100:
           window = 10
       else:
           window = 2
       step = fileSize / window
       fileBuffer = [None]*window
       index = 0
       segment = '$'
       print(fileSize)
       while 1:
           segment =file_dl.read(step)
           if segment == '':
               break
           fileBuffer[index] = file_dl.read(step)
           index+=1
       return (window, fileBuffer, step, 1)
    except:
        raise
        return 0
    
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
        fileSize, fileBuffer, step, condition = fileExists(params)
        print(fileBuffer)
        if request == "get" and condition!= 0:
            serverSocket.sendto("%d:%s"%(fileSize, fileBuffer[ackCount]), clientAddrPort)
            state = _S_WAIT
        elif request == "get" and condition !=0:
            serverSocket.sendto("404", clientAddrPort)
            state = _S_INIT
        else: 
            serverSocket.sendto("close", clientAddrPort)
            state = _S_INIT
        
    elif state == _S_WAIT:  
        if request == "ack":
            if params == ackCount:
                ackCount += 1
                if ackCount >= len(fileBuffer) or fileBuffer[ackCount] == None:
                    serverSocket.sendto("close", clientAddrPort)
                    state = _S_INIT
                    ackCount = 0
                elif fileBuffer[ackCount] != None:
                    serverSocket.sendto(fileBuffer[ackCount], clientAddrPort)
                    state = _S_WAIT 
            elif params < ackCount and params >= 0 and fileBuffer[ackCount] != None:
                serverSocket.sendto(fileBuffer[params], clientAddrPort)
                state = _S_WAIT
                
        elif request == "get":
            # Case where the server answer for data[0] was lost after client started get
            if fileExists(params):
                serverSocket.sendto(fileBuffer[0], clientAddrPort)
                state = _S_WAIT
            elif not fileExists(params):
                serverSocket.sendto("404", clientAddrPort)
                state = _S_INIT
                
    print(state);
    
