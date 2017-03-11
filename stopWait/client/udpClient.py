#! /bin/python
#Can Transmit 1m data
import sys, re  
from socket import *
import json
from array import array
#prototypes and functions
print sys.path
def buildRequest(requset, param):
    return json.dumps({'request':requset, 'params':param})
def usage():
    print "usage: %s --request [get 'or' put] --serverAddr [host:port] -f [filename]"  % sys.argv[0]
    sys.exit(1)

#constants
_C_INIT = "c_initial"       # state definition: initial
_C_WAIT = "c_waiting"       # state definition: waiting for data
_C_ACK = "c_acking"         # state definition: accepting data

#object fields
serverAddr = ('', 50000)
initRequest = buildRequest("get", "file1.txt")
state = _C_INIT             # current state
ackCount = 0                # count of successful transmit
timeout = 2              # timeout for socket thread 
packegeDropCount = 0
buffer = []
bufferSize = 0.0
tau = 2.5 #max timeout
#requests and usage
try:
    args = sys.argv[1:]
    while args:
        sw = args[0]; del args[0]
        if sw == "--request":
            request = re.split("", args[0]); del args[0]
            if request != "put" or request != "get":
                print "unexpected request ->  %s" % args[0]
                usage()
            initRequest = buildRequest(request, fileName)
        if sw == "--serverAddr":
            addr, port = re.split(":", args[0]); del args[0]
            serverAddr = (addr, int(port))
        if sw == "-f":
            fileName = re.split("", args[0]); del args[0]
        else:
            print "unexpected parameter %s" % args[0] 
            usage()         
except:
    usage()

while 1: #Finite State Machine, Look at graphs and FSM pictures
    print("sending")
    print ("state: %s" % state)
    print ("ack[%s]" % ackCount)
    if timeout > tau:
        print('excesive timeout')
    if state == _C_INIT:
        message = initRequest     
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
        #Slidding Window
        packegeDropCount += .005
        timeout +=  packegeDropCount
    else:
        if response == "close":
            print("file transmission is over")
            break;
        elif response == "404":
            print ("404, unknown file")
            usage()
            break;
        elif state == _C_INIT:
            responseArguments= response.split('::')
            bufferSize = int(responseArguments[0])
            buffer = [None]*bufferSize
            buffer[0] = responseArguments[1]
            state = _C_ACK
            #Slidding Window
            if bufferSize >=500:
                timeout = 4
                tau = 12
            elif bufferSize >=50:
                timeout = .4
                tau = 1.2
            else:
                timeout = .04
                tau = .5
        elif state == _C_WAIT:
            state = _C_ACK
        elif state == _C_ACK:
            buffer[ackCount] = response
            ackCount += 1
            state = _C_ACK
        progress = (float(ackCount)/bufferSize)*100
        print("package: %d of %d progress:%f %%" % (ackCount, bufferSize, progress))
        clientSocket.close()
print("full msg")

print(filter(None, buffer))
        
       
       
    