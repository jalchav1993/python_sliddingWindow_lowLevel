#! /bin/python
#! /Users/aexchv/Desktop/Nets/udp-file-transfer-coreunlimied/jsonParse.py
# ref:https://docs.python.org/2/library/re.html
# @name Json Parser Unit Tester
# @author Jesus Chavez

from jsonParse import *
import json

#json api
def buildRequest(request, param):
    return json.dumps({'request':request, 'params':param})
    
#json api
def extractRequest(input):
    return json.loads(input)

#testing json loads
def testParsing(request, params):
    expected = buildRequest(request, params)
    actual = jsonParseThis(request, params)
    print "expected %s \n"%expected
    print "actual %s \n"%actual
    return actual == expected
    
def testDeparsing(request, params):
    in_expected = buildRequest(request, params)
    in_actual = jsonParseThis(request, params)
    expected = extractRequest(in_expected)
    actual = jsonDeParseThis(in_actual)
    print "expected %s \n"%expected
    print "actual %s \n"%actual
    return actual == expected
    
print "testing parsing 'put', 'file.txt' %s" % testParsing("put", "file.txt")
print "testing deparsing 'put', 'file.txt' %s" % testDeparsing("put", "file.txt")
print "testing parsing 'ack', '0' %s" % testParsing("ack", "0")
print "testing deparsing 'ack', '0' %s" % testDeparsing("ack", "0")
