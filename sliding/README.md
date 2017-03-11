Author Jesus Chavez
I added my own json parser using split and regular expressions, I used the python documentation,
ref:https://docs.python.org/2/library/re.html
The protocol is able to get files up to 1 mb, using sliding window.
My algorithm goes as fallows:
- serverside:
-- initial state wait for a get request with file name
-- when the server gets that requests check if file exists, send 404 if not, otherwise respond with number of segments to be downloaded and first segment. This is the sliding window, the server calculates the number of segments by file size as this:
       window = 10
       if fileSize > 10000:
           window = 1000
       elif fileSize > 1000:
           window = 100
       elif fileSize >100:
           window = 10
       else:
           window = 2
-- the client gets this measurement to report download percentage %