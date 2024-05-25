#!/usr/bin/env python3


import logging
import os
import json

from fastf1.livetiming.clientmod2 import SignalRClientMod2

# Load config from /config/config.json into individual variables
import json

try:
    # Open the JSON file and load the data into a Python dictionary
    with open('/config/config.json') as f:
        data = json.load(f)

    # Assign the data to individual variables
    WLED_GREEN = data['wled_green']
    WLED_YELLOW = data['wled_yellow']
    WLED_RED = data['wled_red']
    WLED_SC = data['wled_sc']
    WLED_CHEQUERED = data['wled_checkered']
    WLED_TRACKCLEAR = data['wled_trackclear']
    WLED_HOST = data['wled_host']
    WLED_DELAY = data['wled_delay']
    
except FileNotFoundError:
    print("Error: The file /config/config.json was not found.")
except json.JSONDecodeError:
    print("Error: The file /config/config.json does not contain valid JSON.")
except KeyError as e:
    print(f"Error: The key {e} was not found in the JSON data.")



"""
# Set up environment variables
WLED_HOST=str(os.getenv('WLED_HOST', '')) # IP Address of WLED
WLED_GREEN=str(os.getenv('WLED_GREEN', 1)) # Preset ID for Green
WLED_TRACKCLEAR=str(os.getenv('WLED_TRACKCLEAR', 7)) # Preset ID for Track Clear
WLED_YELLOW=str(os.getenv('WLED_YELLOW', 2)) # Preset ID for Yellow
WLED_RED=str(os.getenv('WLED_RED', 3)) # Preset ID for Red
WLED_CHEQUERED=str(os.getenv('WLED_CHEQUERED', 4)) # Preset ID for Chequered
WLED_SC=str(os.getenv('WLED_SC', 5)) # Preset ID for Safety Car
"""

# Set up logging
log = logging.getLogger()
log.setLevel(logging.DEBUG)

client = SignalRClientMod2(filename="output.txt", WLED_GREEN=WLED_GREEN, WLED_TRACKCLEAR=WLED_TRACKCLEAR, WLED_YELLOW=WLED_YELLOW, WLED_RED=WLED_RED, WLED_CHEQUERED=WLED_CHEQUERED, WLED_SC=WLED_SC, WLED_HOST=WLED_HOST, WLED_DELAY=WLED_DELAY, debug=False)
#client = SignalRClientMod(filename="output.txt", debug=False)

client.start()
