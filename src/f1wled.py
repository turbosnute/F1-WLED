"""Using the Fast-F1 signalr client?
======================================

Demonstrates the usage of the SignalRClient
"""
import logging

from fastf1.livetiming.clientmod import SignalRClientMod


log = logging.getLogger()
log.setLevel(logging.DEBUG)

client = SignalRClientMod(filename="output.txt", debug=True)
client.start()
