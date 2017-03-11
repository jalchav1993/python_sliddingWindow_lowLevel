#! /bin/python
# ref:https://docs.python.org/2/library/re.html
# @name Json Parser
# @author Jesus Chavez
# @funct jsonParseThis() manual parser for json inputs 
# @return python representation of json
import sys, re  
def jsonParseThis(request, params):
    return "{'request':'%s', 'params':'%s'}" % (request, params)
# ref:https://docs.python.org/2/library/re.html
# @name Json Parser
# @author Jesus Chavez
# @funct jsonParseThis() manual parser for json inputs 
# @return python representation of json
def jsonDeParseThis(input):
    #print input
    #m = re.match(r"(?P<request>\w+) (?P<params>\w+)", input)
    #m.groupdict()
    m = re.match(r"{'request':'(?P<request>\w+)', 'params':'(?P<params>\w+)'}", input)
    return m.groupdict()

