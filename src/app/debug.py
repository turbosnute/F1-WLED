import logging
import os
import json

from fastf1.livetiming.clientmod2 import SignalRClientMod2


data = json.load(open('/config/config.json'))

WLED_GREEN = data['wled_green']
WLED_YELLOW = data['wled_yellow']
WLED_RED = data['wled_red']
WLED_SC = data['wled_sc']
WLED_CHEQUERED = data['wled_checkered']
WLED_TRACKCLEAR = data['wled_trackclear']
WLED_HOST = data['wled_host']
WLED_DELAY = data['wled_delay']