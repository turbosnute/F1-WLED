#!/usr/bin/env python3

import logging
import os
import json

from fastf1.livetiming.clientmod2 import SignalRClientMod2

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

# Set up logging
log = logging.getLogger()
log.setLevel(logging.DEBUG)

client = SignalRClientMod2(WLED_GREEN=WLED_GREEN, WLED_TRACKCLEAR=WLED_TRACKCLEAR, WLED_RED=WLED_RED, WLED_YELLOW=WLED_YELLOW, WLED_CHEQUERED=WLED_CHEQUERED, WLED_SC=WLED_SC, WLED_HOST=WLED_HOST, WLED_DELAY=WLED_DELAY, debug=True)

client.start()
