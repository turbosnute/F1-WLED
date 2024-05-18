#!/usr/bin/env python3


import logging
import os

from fastf1.livetiming.clientmod2 import SignalRClientMod2


# Set up environment variables
WLED_HOST=str(os.getenv('WLED_HOST', '')) # IP Address of WLED
WLED_GREEN=str(os.getenv('WLED_GREEN', 1)) # Preset ID for Green
WLED_TRACKCLEAR=str(os.getenv('WLED_TRACKCLEAR', 7)) # Preset ID for Track Clear
WLED_YELLOW=str(os.getenv('WLED_YELLOW', 2)) # Preset ID for Yellow
WLED_RED=str(os.getenv('WLED_RED', 3)) # Preset ID for Red
WLED_CHEQUERED=str(os.getenv('WLED_CHEQUERED', 4)) # Preset ID for Chequered
WLED_SC=str(os.getenv('WLED_SC', 5)) # Preset ID for Safety Car

# Set up logging
log = logging.getLogger()
log.setLevel(logging.DEBUG)

client = SignalRClientMod2(filename="output.txt", WLED_GREEN=WLED_GREEN, WLED_TRACKCLEAR=WLED_TRACKCLEAR, WLED_YELLOW=WLED_YELLOW, WLED_RED=WLED_RED, WLED_CHEQUERED=WLED_CHEQUERED, WLED_SC=WLED_SC, WLED_HOST=WLED_HOST, debug=True)
#client = SignalRClientMod(filename="output.txt", debug=False)

client.start()
