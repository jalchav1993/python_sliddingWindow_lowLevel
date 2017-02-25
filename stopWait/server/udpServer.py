#! /bin/python
from socket import *
import sys

state = "init"
# default params
serverAddr = ("", 50001)

print "binding datagram socket to %s" % repr(serverAddr)
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(serverAddr)
print "ready to receive"
while 1:
    request, clientAddrPort = serverSocket.recvfrom(2048)
    print "from %s: rec'd '%s'" % (repr(clientAddrPort), message)
    
    if request == "get:%s":
        modifiedMessage = message.upper()
        serverSocket.sendto("ack_filename", clientAddrPort)