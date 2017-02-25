#! /bin/python
import time
import sys, re  
from socket import *
from threading import Thread 
# default params
serverAddr = ('localhost', 50001)       

#file location
fileLoc = '~/'
                       
def run(conditions):
    state = conditions['request']
    filename = conditions['filename']
    serverAddr = conditions['serverAddr']
    data = ""

    while state != "close":
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        clientSocket.settimeout(5)
        if state == "get": 
            try:
                clientSocket.sendto("get:%s" % filename, serverAddr)
                response, serverAddrPort = clientSocket.recvfrom(2048)
                if response == "ack_filename":
                    state = "wait_data"
            except timeout:
                print("timedout, trying again")
        if state == "wait_data":
            clientSocket.sendto("", serverAddr)
            response, serverAddrPort = clientSocket.recvfrom(2048)
            #if response != "":
            state = "ack_data"
            data = response
        if state == "ack_data":
            clientSocket.sendto("", serverAddr)
            response, serverAddrPort = clientSocket.recvfrom(2048)
            #if response == "close":
            state = "close"
        print(timeout);
        #time.sleep(timeout)
        clientSocket.close()
        
conditions = {'request':'get', 
    'filename':'testfile.txt', 
    'serverAddr': ('localhost', 50001)
    }

t = Thread(target=run, args=(conditions,))
t.start()