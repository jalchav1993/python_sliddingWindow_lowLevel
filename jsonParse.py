#! /bin/python
# ref:https://docs.python.org/2/library/re.html
# @name Json Parser
# @author Jesus Chavez
# @funct jsonParseThis() manual parser for json inputs 
# @return python representation of json
import sys, re  
def jsonParseThis(request, params):
    return "{request:%s, params:%s}" % (request, params)
def jsonDeParseThis(request, params):
    return "{request:%s, params:%s}" % (request, params)

