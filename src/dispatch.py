import time
import config
import logging
import os

class dispatcher:

    def __init__(self, sourcequeue, httpqueue, parser, relay = False):
        
        self.http = False
        self.tim = False

        self.sourcequeue = sourcequeue
        self.httpqueue = httpqueue
        self.sent = []
        self.parser = parser
        self.relay = relay

    def run(self):
        
        while True:
            
            try:
                
                while self.sourcequeue:
                    
                    logging.info('Message received')
                    rxmsg = self.sourcequeue.popleft()
                    logging.debug('Processing %s from queue' % rxmsg)
                    
                    if rxmsg not in self.sent:

                        logging.info('Dispatching message')
                        
                        #PARSE
                        logging.debug('Parsing message')
                        pmsg = self.parser.parse(rxmsg)

                        #RELAY
                        if self.relay != False:
                            logging.info('Triggering Relay')
                            self.relay.trigger()

                        #HTTP
                        if self.http and pmsg != False:
                            logging.debug('Queue for HTTP dispatch: %s' % pmsg)
                            self.httpqueue.append(pmsg)

                        #TIM
                        if self.tim:

                            logging.debug('Sending message to TIM')
                            
                            try:                            
                                print('====== TIM OUTPUT ======')
                                os.system('TurnOutClient.exe %s "%s"' % (self.capcode, rxmsg))
                                print('========================')
                                logging.debug('Sent %s to TIM' % rxmsg)
                            except:
                                logging.exception('Failed to send %s to TIM' % rxmsg)
                        
                        self.sent.append(rxmsg)
                        logging.debug('Logging as Dispatched: %s' % rxmsg)

                    else:
                        
                        logging.info('Message already dispatched')
                        
            except IndexError:
                    pass
            #Pause
            time.sleep(0.1)
