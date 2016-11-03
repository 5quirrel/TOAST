#!/usr/bin/env python
#! python3

import asyncio
import websockets
import datetime
import random
import json
import logging

class server():

    def __init__(self, httpqueue):

        self.httpqueue = httpqueue
        

    def run(self):
        
        async def sendinc(websocket, path):
            while True:
                now = datetime.datetime.utcnow().isoformat() + 'Z'
                if self.httpqueue:
                    logging.debug('Sending websocket message')
                    wsmsg = self.httpqueue.popleft()
                    await websocket.send(json.dumps(wsmsg))
                await asyncio.sleep(1)

        start_server = websockets.serve(sendinc, '0.0.0.0', 5678)
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
