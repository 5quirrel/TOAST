import config
import time
import logging
import threading
import dispatch
import parsers
import relays
import msg.sms
import msg.pdt
import toasthttp.serverflask
import toasthttp.serverws
from logging.config import fileConfig
from collections import deque

#Start logging based on logging.conf
fileConfig('settings/logging.conf')
logger = logging.getLogger()

logging.info('TOAST %s' % config.ver)

#Define Message Queues

logging.debug('Creating messaging queues')
incoming = deque([])
httpoutgoing = deque([])

#Define Message Parser class

logging.debug('Defining Parser')
parser = parsers.parser()
parser.settingspath = config.settingspath

#HTTP

if config.http:
    
    logging.debug('Configuring WebSocket')
    ws = toasthttp.serverws.server(httpoutgoing)

    logging.info('Starting WebSocket Server')
    t_ws = threading.Thread(target=ws.run)
    t_ws.daemon = True
    t_ws.start()

    logging.debug('Configuring Flask')
    flask = toasthttp.serverflask.server()
    flask.systemname = config.systemname
    flask.systemip = config.systemip
    flask.alert = config.alert
    flask.alerttype = config.alerttype

    logging.info('Starting Flask Server')
    t_flask = threading.Thread(target=flask.run)
    t_flask.daemon = True
    t_flask.start()

else:

    logging.debug('HTTP disabled')

#PDT

if config.pdt:

    logging.debug('Configuring PDT device')
    pdt = msg.pdt.pdtdevice(config.pdtcom, incoming)
        
    logging.info('Starting PDT Monitor')
    t_pdt = threading.Thread(target=pdt.monitor)
    t_pdt.daemon = True
    t_pdt.start()

else:
    
    logging.debug('PDT disabled')

#SMS

if config.sms:

    logging.debug('Configuring SMS device')
    sms = msg.sms.smsdevice(config.smscom, incoming, config.smswhitelist)
        
    logging.info('Starting SMS Monitor')
    t_sms = threading.Thread(target=sms.monitor)
    t_sms.daemon = True
    t_sms.start()

else:
    
    logging.debug('PDT disabled')

#RELAY

if config.relay:

    logging.debug('Configuring Relay device')
    if config.relaytype == 'CBW-QUAD':
        relay = relays.cbwquad(config.relayip, config.relayport)
        relay.outputs = {'1': config.relayoutput1,
                         '2': config.relayoutput2,
                         '3': config.relayoutput3,
                         '4': config.relayoutput4}
else:

    logging.debug('Relay disabled')
    relay = False

#DISPATCHER

logging.info('Starting Message Dispatcher')
dispatch = dispatch.dispatcher(incoming, httpoutgoing, parser, relay)
dispatch.http = config.http
dispatch.tim = config.tim
dispatch.capcode = config.capcode
t_dispatcher = threading.Thread(target=dispatch.run)
t_dispatcher.daemon = True
t_dispatcher.start()

#TEST MODE

if config.testmode:

    testmessages = []
    
    with open('settings\\test_messages.txt', 'r') as f:
        testmessages = (f.read().splitlines())

    for m in testmessages:
        logging.info('Sending test message : %s' % m)
        incoming.append(m)
        time.sleep(30)

print("Use CTRL-C to Quit")

while True:

    time.sleep(1)
