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

client = SignalRClientMod2(filename="output.txt", WLED_GREEN=WLED_GREEN, WLED_TRACKCLEAR=WLED_TRACKCLEAR, WLED_YELLOW=WLED_YELLOW, WLED_RED=WLED_RED, WLED_CHEQUERED=WLED_CHEQUERED, WLED_SC=WLED_SC, WLED_HOST=WLED_HOST, WLED_DELAY=WLED_DELAY, debug=False)
#client = SignalRClientMod(filename="output.txt", debug=False)

msgtype1 = "{'C': 'd-574D6C21-B,0|sJE,0|sJF,3|d,2A7|BK,30', 'M': [{'H': 'Streaming', 'M': 'feed', 'A': ['Heartbeat', {'Utc': '2024-05-18T14:59:16.0296373Z', '_kf': True}, '2024-05-18T14:59:14.01Z']}]}"

msgtype2 = '["RaceControlMessages", {"Messages": {"26": {"Utc": "2024-05-26T13:04:08", "Lap": 1, "Category": "Flag", "Flag": "CLEAR", "Scope": "Sector", "Sector": 11, "Message": "CLEAR IN TRACK SECTOR 11"}}}, "2024-05-26T13:04:07.961Z"]'

msgtype3 = "{'C': 'd-574D6C21-B,0|sJE,0|sJF,3|d,2AA|BK,31', 'M': [{'H': 'Streaming', 'M': 'feed', 'A': ['RaceControlMessages', {'Messages': {'24': {'Utc': '2024-05-18T15:00:00', 'Category': 'Flag', 'Flag': 'CHEQUERED', 'Scope': 'Track', 'Message': 'CHEQUERED FLAG'}}}, '2024-05-18T15:00:00.199Z']}]}"

client.handle_message(msgtype1)

client.handle_message(msgtype2)

client.handle_message(msgtype3)