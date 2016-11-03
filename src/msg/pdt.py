import serial
import logging
import time
import re

class pdtdevice:

    def __init__(self, com, queue):
        self.modem = serial.Serial(com, 9600, timeout=1)
        self.queue = queue

    def monitor(self):
        while True:
            while self.modem.in_waiting != 0:
                pdtrx = []
                logging.debug('PDT received data')
                pdtrxline = self.modem.readline().decode()
                logging.debug('Read line "%s"' % pdtrxline)
                
                try:
                    pdtrx = re.search('\d+ A (.*)',pdtrxline).group(1)
                    pdtrx = pdtrx.rstrip()
                    self.queue.append(pdtrx)
                    logging.info('PDT RX: %s' % pdtrx)
                
                except AttributeError:
                    logging.debug('Search string not found in "%s"' % pdtrxline)
                    continue
                
            time.sleep(0.1)
