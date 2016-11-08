#! python3

import logging
import time
import re
import configparser
import sys
import csv
import socket
from logging.config import fileConfig

#Read config
configfile = configparser.ConfigParser()

#Set version
ver = '1.0 Beta'

#Check for config section
if configfile.read('settings\\config.ini') == []:
    logging.critical('Config file not found, check for config.ini')
    sys.exit()

#GENERAL
systemname = configfile.get('GENERAL','SYSTEMNAME')

systemip = configfile.get('GENERAL','SYSTEMIP')
if systemip == 'AUTO':
    systemip = socket.gethostbyname(socket.gethostname())

locale = configfile.get('GENERAL','LOCALE')
if locale == 'NONE':
    settingspath = 'settings\\'
else:
    settingspath = 'settings\\locales\\%s\\' % locale

testmode = configfile.getboolean('GENERAL','TESTMODE')

#DISPATCH
intermessagedelay = configfile.getint('DISPATCH','INTERMESSAGEDELAY')
dropduplicates = configfile.getboolean('DISPATCH', 'DROPDUPILICATES')

#TIM
tim = configfile.getboolean('TIM', 'ENABLED')
capcode = configfile.get('TIM','CAPCODE')

#HTTP
http = configfile.getboolean('HTTP', 'ENABLED')
alert = configfile.get('HTTP','ALERT')
alerttype = configfile.get('HTTP','ALERT').split(sep='.')[-1]

if alerttype == 'mp3':
    alerttype = 'mpeg'

#PDT
pdt = configfile.getboolean('PDT', 'ENABLED')
pdtcom = configfile.get('PDT','COM')

#SMS
sms = configfile.getboolean('SMS', 'ENABLED')
smscom = configfile.get('SMS','COM')
smsack = configfile.getboolean('SMS', 'SMSACK')
smsacknum = configfile.get('SMS','ACKNUM')
smswhitelist = configfile.get('SMS','WHITELIST').split(',')

#RELAY
relay = configfile.getboolean('RELAY','ENABLED')
relayip = configfile.get('RELAY','IP')
relayport = configfile.getint('RELAY','PORT')
relaytype = configfile.get('RELAY','TYPE')
relayoutput1 = configfile.getboolean('RELAY','OUTPUT1')
relayoutput2 = configfile.getboolean('RELAY','OUTPUT2')
relayoutput3 = configfile.getboolean('RELAY','OUTPUT3')
relayoutput4 = configfile.getboolean('RELAY','OUTPUT4')
