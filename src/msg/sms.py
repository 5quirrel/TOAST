import logging
import serial
import time
import datetime
import re
from messaging.sms import SmsDeliver, SmsSubmit

class smsdevice:

    def __init__(self, com, queue, whitelist):
        self.modem = serial.Serial(com, 115200, timeout=1)
        self.queue = queue
        self.whitelist = whitelist

    def command(self, command):
        
        self.modem.write(command.encode())
        self.modem.write('\r'.encode())
        time.sleep(0.2)

    def readline(self):

        return self.modem.readline().decode()

    def send(self, message):
        
        #Enter text mode
        self.command('AT+CMGF=1')
        self.command('AT+CMGS="%s"\r' % number)
        time.sleep(0.2)
        self.command('%s\x1A' % message)
        time.sleep(0.2)
        #Revert to PDU
        self.command('AT+CMGF=0')

    def inmem(self):
        
        #Set to PDU mode
        self.command('AT+CMGF=0')
        #Check for all messages stored and add storage positions to list to be returned
        self.command('AT+CMGL=4')
        #Make a list
        smsinmem = []
        memreadline = self.readline()
        while memreadline != '':
            try:
                smsinmem.append(re.search('\+CMGL: (\d+),',memreadline).group(1))
            except AttributeError:
                pass
            memreadline = self.readline()
        return smsinmem

    def monitor(self):

        while True:
            
            #Create SMS process and storage dictionaries
            smsparts = {}
            smsmemloc = {}
            smsseqcount = {}
            if self.inmem() != []:
                logging.debug('Message found in memory, waiting briefly for stragglers')
                #Wait time
                time.sleep(15)
                processlocations = self.inmem()
                logging.debug('SMSinmem returned list %s processing now' % processlocations)
                for loc in processlocations:
                    #Send message to retrive message
                    logging.debug('Reading SMS in memory location %s' % loc)
                    self.command('AT+CMGR='+loc)
                    #Retrive and store for processing
                    pdu = re.search('CMGR: \d+,,\d+\r\n(\w*)\r\n\r\nOK',self.modem.read(self.modem.in_waiting).decode()).group(1)
                    #Process into SMS class
                    sms = SmsDeliver(pdu)

                    #Check if sender is on whitelist
                    logging.debug('Checking whitelist')
                    if sms.number not in self.whitelist:
                        logging.warning('Number %s not in whitelist, dropping this message!' % sms.number)
                        self.command('AT+CMGD='+loc)
                        continue
                    
                    #Check for single part message and process if so
                    if 'cnt' not in sms.data:
                        logging.debug('Did not find count in UDH of SMS (not a concatenated SMS)')
                        logging.debug('Working with SMS from : %s at %s' % (sms.number, str(sms.date)))
                        check = 0
                        while check <= 5:
                            checktag = sms.number + str(sms.date - datetime.timedelta(seconds=check))
                            logging.debug('Looking for %s in SMS tags' % checktag)
                            if checktag in smsparts:
                                logging.debug('Found exsisting tag within range at %s sec old - (%s) %s appending %s' % (check, checktag, smsparts[checktag][1], sms.text))
                                smsparts[checktag][1] += ' '+sms.text
                                smsmemloc[checktag].append(loc)
                                break
                            check += 1
                        else:
                            smstag = sms.number + str(sms.date)
                            logging.debug('Did not find matching tag within range. Making new tag for (%s) %s' % (smstag, sms.text))                    
                            smsparts[smstag] = {}
                            smsparts[smstag][1] = sms.text
                            smsseqcount[smstag] = 1
                            smsmemloc[smstag] = []
                            smsmemloc[smstag].append(loc)
                    else:
                        #Continue for Multi-Part SMS
                        logging.debug('Found CONCAT SMS')
                        #Make a dictionary key is one doesn't exsist
                        if sms.udh.concat.ref not in smsparts:
                            smsparts[sms.udh.concat.ref] = {}
                        if sms.udh.concat.ref not in smsmemloc:
                            smsmemloc[sms.udh.concat.ref] = []
                        #Store into processing and sequence count dictionary
                        smsparts[sms.udh.concat.ref][sms.udh.concat.seq] = sms.text
                        smsseqcount[sms.udh.concat.ref] = sms.udh.concat.cnt
                        smsmemloc[sms.udh.concat.ref].append(loc)
                    logging.debug('SMS memory processing complete, waiting before next check')
                
            #Process into complete messages if all parts received
            smsrx = []
            for ref in list(smsparts):
                #Reset compiledsms
                compiledsms = ''
                #Check if all parts are rx and combine is they are
                if len(smsparts[ref]) == smsseqcount[ref]:
                    #Process each sequence into a long string
                    logging.debug('Processing SMS %s' % ref)
                    for seq in sorted(smsparts[ref]):
                        #add to string
                        compiledsms += smsparts[ref][seq]
                        logging.debug('Compiling SMS %s' % compiledsms)
                    logging.info('SMS RX: %s' % compiledsms)
                    smsrx.append(compiledsms)
                    #Delete sequence count
                    del smsseqcount[ref]
                    #Delete parts in dictionary
                    del smsparts[ref]
                    #Delete SMS in modem
                    for i in smsmemloc[ref]:
                        #Delete the message
                        logging.debug('Deleting SMS message in memory position %s' % i)
                        self.command('AT+CMGD='+i)
                    del smsmemloc[ref]
                    
            #Return compiled SMS list or False
            self.queue.extend(smsrx)

