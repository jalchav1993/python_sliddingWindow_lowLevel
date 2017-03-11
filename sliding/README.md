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
-- the program increments the ack counter when it gets a new ack, ignores already acknoledged ack requestes, will only change state in a new request
-- the client gets this measurement to report download percentage 
-client side:
-- the client will send a get request with a filename
-- when the server responds with init segment and the size of the window, the client will set up
the initial timeout(will be incremented as packeges are lost) and maxtimeout (to test when the timeout was incremented exponentially and needs to break from loop because of likely unsuccesful app) 
            if bufferSize >=500:
                timeout = 4
                tau = 12
            elif bufferSize >=50:
                timeout = .4
                tau = 1.2
            else:
                timeout = .04
                tau = .5
To test code, run udpClient.py, udpServer.py, and any of the proxy scripts concurrently. The program shows a report with throughput and rtt. Calculated RTT using time.time(). and throughput by dividing rtt over window.