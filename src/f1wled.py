#!/usr/bin/env python3

"""Using the Fast-F1 signalr client?
======================================

Demonstrates the usage of the SignalRClient
"""
import logging
import os

from fastf1.livetiming.clientmod import SignalRClientMod


# Environment Variables
#
#   def __init__(self, filename: str, filemode: str = 'w', debug: bool = False,
#                 timeout: int = 60, logger: Optional = None, WLED_HOST: str, WLED_GREEN: int, WLED_YELLOW: int, WLED_RED: int, WLED_CHEQUERED: int, WLED_SC: int):
# 
WLED_HOST=str(os.getenv('WLED_HOST', '')) # IP Address of WLED
WLED_GREEN=str(os.getenv('WLED_GREEN', 1)) # Preset ID for Green
WLED_YELLOW=str(os.getenv('WLED_YELLOW', 2)) # Preset ID for Yellow
WLED_RED=str(os.getenv('WLED_RED', 3)) # Preset ID for Red
WLED_CHEQUERED=str(os.getenv('WLED_CHEQUERED', 4)) # Preset ID for Chequered
WLED_SC=str(os.getenv('WLED_SC', 5)) # Preset ID for Safety Car

log = logging.getLogger()
log.setLevel(logging.DEBUG)

client = SignalRClientMod(filename="output.txt", debug=True, WLED_HOST=WLED_HOST, WLED_GREEN=WLED_GREEN, WLED_YELLOW=WLED_YELLOW, WLED_RED=WLED_RED, WLED_CHEQUERED=WLED_CHEQUERED, WLED_SC=WLED_SC)
#client = SignalRClientMod(filename="output.txt", debug=False)

client.start()
