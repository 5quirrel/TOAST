import config
import socket
import logging

def httpreq(ip, port, request):

    CRLF = "\r\n"

    request = [
        "GET %s HTTP/0.9" % request,
        "Host: %s:%s" % (ip, port),
        "Connection: Close",
        "",
        "",
    ]

    # Connect to the server
    s = socket.socket()
    s.settimeout(2)
    s.connect((ip, port))

    # Send an HTTP request
    s.send(CRLF.join(request).encode())

    # Get the response (in several parts, if necessary)
    response = ''
    buffer = s.recv(4096).decode()
    while buffer:
        response += buffer
        buffer = s.recv(4096).decode()

    # HTTP headers will be separated from the body by an empty line
    header_data, _, body = response.partition(CRLF + CRLF)

    return header_data

class cbwquad:

    def __init__(self, ip, port):

        self.ip = ip
        self.port = port
        self.outputs = {'1': False, '2': False, '3': False, '4': False}
        
    def trigger(self):
        
        for output in self.outputs:
            if self.outputs[output] == True:
                try:
                    httpreq(self.ip, self.port,'/state.xml?relay%sState=%s' % (output, 2))
                    logging.debug('Triggering Relay @ %s:%s %s' %  (self.ip, self.port, output))
                except:
                    logging.exception('WebRelay Relay Failed')

class cbwwebrelay:

    def __init__(self, ip, port):

        self.ip = ip
        self.port = port
        
    def trigger(self):
        
        try:
            httpreq(self.ip, self.port,'/state.xml?relayState=%s' % 2)
            logging.debug('Triggering Relay @ %s:%s %s' %  (self.ip, self.port))
        except:
            logging.exception('WebRelay Relay Failed')
