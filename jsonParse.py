#! /bin/python
# ref:https://docs.python.org/2/library/re.html
# @name Json Parser
# @author Jesus Chavez
# @funct jsonParseThis() manual parser for json inputs 
# @return python representation of json
import sys, re  
def jsonParseThis(request, params):
    return "{\"params\": \"%s\", \"request\": \"%s\"}" % (params, request)
# ref:https://docs.python.org/2/library/re.html
# @name Json Parser
# @author Jesus Chavez
# @funct jsonParseThis() manual parser for json inputs 
# @return python representation of json
def jsonDeParseThis(input):
    regExpression = re.compile(r"{\"params\": \"(?P<params>\w+)\", \"request\": \"(?P<request>\w+)\"}")
    m = re.match(regExpression, input)
    return m.groupdict()

