#!/usr/bin/env python
#! python3

import logging
from flask import Flask, render_template

class server:

    def __init__(self):

        self.systemname = ''
        self.systemip = ''
        self.alert = ''
        self.alerttype = ''

    def run(self):

        app = Flask(__name__)
        
        @app.route("/")
        def index():
            return render_template('index.html',
                                   title=self.systemname,
                                   systemip=self.systemip,
                                   alert=self.alert,
                                   alerttype = self.alerttype)
        
        app.run('0.0.0.0', 8080)
