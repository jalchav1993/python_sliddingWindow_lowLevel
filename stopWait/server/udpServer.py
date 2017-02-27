#! /bin/python
from socket import *
import sys
import json
    
_S_INIT = 's_init'      #state where the server starts
_S_SEND = 's_send'      #sending data
_S_WAIT = 's_wait'      #waiting for acknoledgement

state = _S_INIT         #init
ackCount = 0;           #number of packets that are known to be delivered

fileBuffer = []         #buffer for the file to be sent
fileSize = 0            #size in chars
step = 0                #size of segment to be sent

def fileExists(params): #opens and reads the file
    try:
       file_dl = open(params, 'r') #for size
       fileSize = len(file_dl.read())
       file_dl.close()
       file_dl = open(params, 'r') #for lines
       window = 10
       if fileSize > 10000:
           window = 1000
       elif fileSize > 1000:
           window = 100
       elif fileSize >100:
           window = 10
       else:
           window = 2
       step = int(float(fileSize) / window)
       fileBuffer = [None]*window #buffer of None objects
       index = 0
       segment = '$'
       while 1:
           segment =file_dl.read(step)
           if segment == '':
               break
           fileBuffer[index] = file_dl.read(step)
           index+=1
       cleanBuffer = filter(None, fileBuffer)
       fileSize = len(cleanBuffer)
       return (fileSize, fileBuffer, step, 1) #tuple with current constraints
       #fileSize is the size in chars
       #fileBuffer is a list of segments to be sent
       #step is the size of the segment
       #1 for condition: true, file successfuly openes
    except:
        raise
        return 0 #false
    
# default params
serverAddr = ("", 50001)

print "binding datagram socket to %s" % repr(serverAddr)

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(serverAddr)

print "ready to receive"

while 1: #Finite State Machine, Look at graphs and FSM pictures
    message, clientAddrPort = serverSocket.recvfrom(2048)
    print "from %s: rec'd '%s'" % (repr(clientAddrPort), message)
    data = json.loads(message)
    request = data['request']
    params = data['params']
    if state == _S_INIT: #init case, no connections
        fileSize, fileBuffer, step, condition = fileExists(params)
        if request == "get" and condition!= 0:
            print(fileSize)
            serverSocket.sendto("%d::%s"%(fileSize, fileBuffer[ackCount]), clientAddrPort)
            state = _S_WAIT
        elif request == "get" and condition !=0:
            serverSocket.sendto("404", clientAddrPort)
            state = _S_INIT
        else: 
            serverSocket.sendto("close", clientAddrPort)
            state = _S_INIT
        
    elif state == _S_WAIT:  #waiting for ack
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
                serverSocket.sendto("%d::%s"%(fileSize, fileBuffer[ackCount]), clientAddrPort)
                state = _S_WAIT
            elif not fileExists(params):
                serverSocket.sendto("404", clientAddrPort)
                state = _S_INIT
                
    print(state);
    
