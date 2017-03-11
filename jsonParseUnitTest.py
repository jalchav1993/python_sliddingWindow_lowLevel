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
def testParsing():
    expected = buildRequest("put", "file")
    actual = jsonParseThis("put", "file")
    print "expected %s \n"%expected
    print "actual %s \n"%actual
    return actual == expected
    
def testDeparsing():
    in_expected = buildRequest("put", "file")
    in_actual = jsonParseThis("put", "file")
    expected = extractRequest(in_expected)
    actual = jsonDeParseThis(in_actual)
    print "expected %s \n"%expected
    print "actual %s \n"%actual
    return actual == expected
    
print "testing parsing %s" % testParsing()
print "testing deparsing %s" % testDeparsing()
