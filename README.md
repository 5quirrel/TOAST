# TOAST *Turn Out Alerting SysTem*

*An open source turn out application designed to assist volunteer emergency services organisations*

## Features

TOAST is an in-station turnout system designed to fill the need for a free and low cost turn out system for volunteer organisations, where the funds to buy larger commercial systems aren't available.

It can be set up by any one with some motivation and basic IT\communications knowledge.

The system is designed to be modular and features can be turned on and off as desired. It can do the whole lot, including relays for operating station lighting, door, sirens, or as little as providing a screen and a map.

TOAST is completely open-source and written 100% in Python 3.5, everything it does is out there for all to see. This makes user enhancement approachable and customisation for your own messaging systems and formats possible.

### Version 1 Release

Here's the feature list for the first release version...

* Low, low price of free! No ongoing costs, totally open source!
* HTTP call information server and clients. Call information displayed in a live locally hosted webpage with map and Text-to-Speech information announcement.
* OpenStreetMaps incident or static image display.
* Text-to-Speech voice announcement of incident via browser.
* Relay triggering for ControlByWeb relay systems.
* Fully compaitable as a message handler for TIMS application.

#### Messaging Input Systems

* Paging (Serial)
* SMS (USB or Serial)

#### Localities

##### Australia, South Australia

Designed for the SAGRN messaging format. TOAST is also compatible for use with the TIMS application and can be used as a message handler to provide TIMS with SMS messaging and relay capabilities.

## Requirements

### General

OS: Windows (Tested on Windows 7), Linux (Untested)

### By Capability

#### SMS

Cellular modem with serial connection (Note: USB modems have Serial COM port access).

#### Paging

Paging device capable of outputting messages via a serial connection.

#### Relays

Supported Relays:

* [ControlByWeb QuadRelay](http://www.controlbyweb.com/webrelay-quad/)
* [ControlByWeb WebRelay](http://www.controlbyweb.com/webrelay/)

#### HTTP

* Networked PC to act as server, accessible to all clients.

##### Browser

|   Feature  | Chrome | IE  | FireFox  | Safari  |
|------------|:------:|:---:|:--------:|:-------:|
| WebSockets |   16   | 11  |    11    |    6    |
| WebSpeech  |   33   |     |    49    |    7    |

## Install Process

* TBA

## Configuration Process

* TBA

### Configuration Files

#### General Config

**settings\config.ini**

#### Mapping Resources

**settings\maps.csv**

Formatted as Reference,Type,Resource,Resource

##### OSM Format

Formatted as Reference,Type,Lat,Long

(e.g. CTY 12 86B,OSM,-34.0000,128.00000)

##### Static Image Format

Reference,Type,Image,

(e.g. CTY 12 86B,IMG,static\maps\CTY_12_86B.png,)

#### Text-to-Speech

##### Responder Abbreviations

**settings\tts_resp.csv**

Formatted as Word,Spoken

(e.g. CTY101,City one zero one)

##### Address Substitutions

**settings\tts_places.csv**

Formatted as Word,Spoken

(e.g. St,Street)

## Future Release Ideas

Feel free to put forward any other ideas as an Enhancement on the issues page of this project.

## Bugs and Issues

Please report any bugs found or crashes experienced on the issues page of this project.

## Credits

### Code and Modules Used

* PySerial (https://pythonhosted.org/pyserial/)
* Flask (http://flask.pocoo.org/)
* WebSockets (https://websockets.readthedocs.io/en/stable/)
* Python-Messaging (https://github.com/onlinecity/python-messaging)