import re
import csv
import logging
import time
import datetime

class parser():
    
    def __init__(self, settingspath):
        
        self.settingspath = settingspath
        self.maprefs = {}
        self.ttsplaces = {}
        self.ttsresp = {}
        
        with open('%smaps.csv' % self.settingspath, 'r') as f:
            csvmaplist = list(csv.reader(f))
            for ref, t, v1, v2 in csvmaplist:
                self.maprefs[ref] = [t, v1, v2]
                
        with open('%stts_places.csv' % self.settingspath, 'r') as f:
            ttsplaces = list(csv.reader(f))
            for spelt, spoken in ttsplaces:
                self.ttsplaces[spelt] = spoken
                
        with open('%stts_resp.csv' % self.settingspath, 'r') as f:
            ttsresp = list(csv.reader(f))
            for spelt, spoken in ttsresp:
                self.ttsresp[spelt] = spoken
                        
    def parse(self, msg):

        #### MESSAGE BREAK DOWN ####

        logging.debug('Parsing Message: %s' % msg)
        
        remsg = re.search('(INC\d+) (\d+\/\d+\/\d+ \d+:\d+) (.*),(.*),(.*),MAP:(.*),TG (.*),\W*(\w.*):',msg)

        try:
            
            event_time = remsg.group(2)
            event_num = remsg.group(1)
            event_type = remsg.group(3)
            event_level = remsg.group(4)
            event_address = remsg.group(5)
            event_mapref = remsg.group(6)
            event_tg = remsg.group(7)
            event_responders = remsg.group(8)
            event_origmsg = msg
            event_rxtime = time.mktime(datetime.datetime.now().timetuple()) * 1000

        except AttributeError:

            logging.exception('Message failed RegEx parsing')
            return False

        #### MAP CODE ####
     
        try:
            
            logging.debug('Finding map reference for %s' % event_mapref)
            
            if self.maprefs[event_mapref][0] == 'IMG':
                logging.debug('Found static image map reference')
                event_maptype = 'IMG'
                event_mapresource = self.maprefs[event_mapref][1]
                event_lat = 'UNKNOWN'
                event_long = 'UNKNOWN'
                
            elif self.maprefs[event_mapref][0] == 'OSM':
                logging.debug('Found OSM map reference')
                event_maptype = 'OSM'
                event_mapresource = 'OSM'
                event_lat = self.maprefs[event_mapref][1]
                event_long = self.maprefs[event_mapref][2]

        except KeyError:
            logging.debug('No map reference found')
            event_maptype = 'UNKNOWN'
            event_mapresource = 'UNKNOWN'
            event_lat = 'UNKNOWN'
            event_long = 'UNKNOWN'

        #### TTS CODE ####

        logging.debug('Parsing TTS')
        
        speechplaces = event_address
        speechresp = event_responders

        for word, spoken in self.ttsplaces.items():
            speechplaces = re.sub(r'\b%s\b' % word, spoken, speechplaces)

        for word, spoken in self.ttsresp.items():
            speechresp = re.sub(r'\b%s\b' % word, spoken, speechresp)

        event_speech = ('%s, %s, %s' % (speechresp, event_type, speechplaces))

        #### SORT ####

        parsed = {'event_time' : event_time,
                  'event_num' : event_num,
                  'event_type' : event_type,
                  'event_level' : event_level,
                  'event_address' : event_address,
                  'event_maptype' : event_maptype,
                  'event_mapresource' : event_mapresource,
                  'event_lat' : event_lat,
                  'event_long' : event_long,
                  'event_mapref' : event_mapref,
                  'event_tg' : event_tg,
                  'event_responders' : event_responders,
                  'event_speech' : event_speech,
                  'event_origmsg' : event_origmsg,
                  'event_rxtime' : event_rxtime}
       
        return parsed

if __name__=="__main__":
    
    p = parser()

    testmessages = []
    
    with open('settings\\test_messages.txt', 'r') as f:
        testmessages = (f.read().splitlines())

    for m in testmessages:
        print('[Parsing]')
        result = p.parse(m)
        print(result)
    

