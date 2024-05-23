import asyncio
import concurrent.futures
import json
import logging
import time

from typing import (
    Iterable,
    Optional
)
from colorama import Fore, Back, Style
import requests

import fastf1
from fastf1.signalr_aio import Connection

def messages_from_raw(r: Iterable):
    """Extract data messages from raw recorded SignalR data.

    This function can be used to extract message data from raw SignalR data
    which was saved using :class:`SignalRClient` in debug mode.

    Args:
        r: Iterable containing raw SignalR responses.
    """
    ret = list()
    errorcount = 0
    for data in r:
        # fix F1's not json compliant data
        data = data.replace("'", '"') \
            .replace('True', 'true') \
            .replace('False', 'false')
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            errorcount += 1
            continue
        messages = data['M'] if 'M' in data and len(data['M']) > 0 else {}
        for inner_data in messages:
            hub = inner_data['H'] if 'H' in inner_data else ''
            if hub.lower() == 'streaming':
                # method = inner_data['M']
                message = inner_data['A']
                ret.append(message)

    return ret, errorcount


class SignalRClientMod:
    """A client for receiving and saving F1 timing data which is streamed
    live over the SignalR protocol.

    During an F1 session, timing data and telemetry data are streamed live
    using the SignalR protocol. This class can be used to connect to the
    stream and save the received data into a file.

    The data will be saved in a raw text format without any postprocessing.
    It is **not** possible to use this data during a session. Instead, the
    data can be processed after the session using the :mod:`fastf1.api` and
    :mod:`fastf1.core`

    Args:
        filename: filename (opt. with path) for the output file
        filemode: one of 'w' or 'a'; append to or overwrite
            file content it the file already exists. Append-mode may be useful
            if the client is restarted during a session.
        debug: When set to true, the complete SignalR
            message is saved. By default, only the actual data from a
            message is saved.
        timeout: Number of seconds after which the client
            will automatically exit when no message data is received.
            Set to zero to disable.
        logger: By default, errors are logged to the console. If you wish to
            customize logging, you can pass an instance of
            :class:`logging.Logger` (see: :mod:`logging`).
    """
    _connection_url = 'https://livetiming.formula1.com/signalr'

    def __init__(self, filename: str, WLED_GREEN: int, WLED_TRACKCLEAR: int, WLED_YELLOW: int, WLED_RED: int, WLED_CHEQUERED: int, WLED_SC: int, WLED_HOST: str = '', filemode: str = 'w', debug: bool = False,
                 timeout: int = 60, logger: Optional = None):

        self.headers = {'User-agent': 'BestHTTP',
                        'Accept-Encoding': 'gzip, identity',
                        'Connection': 'keep-alive, Upgrade'}
        
        #self.topics = ["Heartbeat", "CarData.z", "Position.z",
        #               "ExtrapolatedClock", "TopThree", "RcmSeries",
        #               "TimingStats", "TimingAppData",
        #               "WeatherData", "TrackStatus", "DriverList",
        #               "RaceControlMessages", "SessionInfo",
        #               "SessionData", "LapCount", "TimingData"]

        self.topics = ["Heartbeat", "RaceControlMessages"]
        self.WLED_GREEN = WLED_GREEN
        self.WLED_TRACKCLEAR = WLED_TRACKCLEAR
        self.WLED_YELLOW = WLED_YELLOW
        self.WLED_RED = WLED_RED
        self.WLED_CHEQUERED = WLED_CHEQUERED
        self.WLED_SC = WLED_SC
        self.WLED_HOST = WLED_HOST

        self.debug = debug
        self.filename = filename
        self.filemode = filemode
        self.timeout = timeout
        self._connection = None


        if not logger:
            logging.basicConfig(
                format="%(asctime)s - %(levelname)s: %(message)s"
            )
            self.logger = logging.getLogger('SignalR')
        else:
            self.logger = logger

        self._output_file = None
        self._t_last_message = None

    
    def fix_json(self, msg):
        msg = msg.replace("'", '"') \
            .replace('True', 'true') \
            .replace('False', 'false')
        return msg

    def _to_wled(self, msg):
        # this should contact wled api
        #print(Fore.YELLOW + msg + " <-|-> " + Fore.RESET)
        #Debug:
        print(Fore.CYAN + self.fix_json(msg) + Fore.RESET)

        baseuri = "http://" + self.WLED_HOST + "/win&PL="
        #http://192.168.137.17/win&PL=3


        #Fix and load json
        msg = self.fix_json(msg)
        print(Fore.YELLOW + msg + " <-|-> " + Fore.RESET)
        json_obj = json.loads(msg)

        # Initialize variables
        preset = 0
        messages = None

        if 'R' in json_obj:
            # R
            if 'RaceControlMessages' in json_obj['R']:
                #print(Fore.MAGENTA + "RaceControlMessages" + Fore.RESET)
                #self.logger.info("RaceControlMessages")
                # RaceControlMessages exists!
                if 'Messages' in json_obj['R']['RaceControlMessages']:
                    #print(Fore.MAGENTA + "Messages" + Fore.RESET)
                    #self.logger.info("Messages")
                    # Messages exists!
                    messages = json_obj['R']['RaceControlMessages']['Messages']
            elif 'RaceControlMessage' in json_obj:
                print(Back.RED, Fore.BLACK, "TYPE 2 TYPE 2", Fore.RESET, Back.RESET)
                messages = json_obj['RaceControlMessage']['Messages']

            for message in messages:
                #print(Fore.MAGENTA + "Message" + Fore.RESET)
                #self.logger.debug("Message")
                # Loop through messages
                if message['Category'] == 'Flag':
                    if message['Flag'] == 'GREEN':
                        print(Fore.GREEN + "Green Flag" + Fore.RESET + " " + message['Message'])
                        preset = self.WLED_GREEN
                    elif message['Flag'] == 'YELLOW' or message['Flag'] == 'DOUBLE YELLOW':
                        print(Fore.YELLOW + "Yellow Flag" + Fore.RESET + " " + message['Message'])
                        preset = self.WLED_YELLOW
                    elif message['Flag'] == 'RED':
                        print(Fore.RED + "Red Flag" + Fore.RESET)
                        preset = self.WLED_RED
                    elif message['Flag'] == 'CLEAR':
                        if message['Message'] == 'TRACK CLEAR':
                            print(Fore.CYAN + "Clear Flag" + Fore.RESET + " " + message['Message'])
                            preset = self.WLED_TRACKCLEAR
                        else:
                            print(Back.CYAN + Fore.Black + message['Message'] + Fore.RESET + Back.RESET)
                            preset = 0
                    elif message['Flag'] == 'CHEQUERED':
                        print(Fore.MAGENTA + "Chequered Flag" + Fore.RESET + " " + message['Message'])
                        preset = self.WLED_CHEQUERED
                    else:
                        preset = 0
                        print(Fore.MAGENTA + message['Message'] + Fore.RESET)
                elif message['Category'] == 'SafetyCar':
                    print(Back.YELLOW + "Safety Car" + Back.RESET + " " + message['Message'])
                    preset = self.WLED_SC
                else:
                    preset = 0
                # Build the URL
                url = "http://" + self.WLED_HOST + "/win&PL=" + str(preset)
                # Send the GET request
                if self.WLED_HOST != '' and preset != 0:
                    try:
                        print(Fore.RED, url, Fore.RESET)
                        #Try to send a GET request
                        response = requests.get(url, timeout=1)
                        #time.sleep(3)
                    except requests.exceptions.RequestException as e:
                        # Handle the exception
                        continue
                elif self.WLED_HOST == '':
                    print("WLED_HOST not set")

    def _to_file(self, msg):
        self._output_file.write(msg + '\n')
        self._output_file.flush()

    async def _on_do_nothing(self, msg):
        # just do nothing with the message; intended for debug mode where some
        # callback method still needs to be provided
        pass

    async def _on_message(self, msg):
        self._t_last_message = time.time()
        loop = asyncio.get_running_loop()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            await loop.run_in_executor(
                pool, self._to_wled, str(msg)
            )

    async def _on_debug(self, **data):
        if 'M' in data and len(data['M']) > 0:
            self._t_last_message = time.time()

        loop = asyncio.get_running_loop()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            await loop.run_in_executor(
                pool, self._to_wled, str(data)
            )

    async def _run(self):
        self._output_file = open(self.filename, self.filemode)
        # Create connection
        session = requests.Session()
        session.headers = self.headers
        self._connection = Connection(self._connection_url, session=session)

        # Register hub
        hub = self._connection.register_hub('Streaming')

        if self.debug:
            # Assign error handler
            self._connection.error += self._on_debug
            # Assign debug message handler to save raw responses
            self._connection.received += self._on_debug
            hub.client.on('feed', self._on_do_nothing)
            # need to connect an async method
        else:
            # Assign hub message handler
            hub.client.on('feed', self._on_message)

        hub.server.invoke("Subscribe", self.topics)

        # Start the client
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            await loop.run_in_executor(pool, self._connection.start)

    async def _supervise(self):
        self._t_last_message = time.time()
        while True:
            if (self.timeout != 0
                    and time.time() - self._t_last_message > self.timeout):
                self.logger.warning(f"Timeout - received no data for more "
                                    f"than {self.timeout} seconds!")
                self._connection.close()
                return
            await asyncio.sleep(1)

    async def _async_start(self):
        self.logger.info(f"Starting FastF1 live timing client "
                         f"[v{fastf1.__version__}]")
        await asyncio.gather(asyncio.ensure_future(self._supervise()),
                             asyncio.ensure_future(self._run()))
        self._output_file.close()
        self.logger.warning("Exiting...")

    def start(self):
        """Connect to the data stream and start writing the data to a file."""
        try:
            asyncio.run(self._async_start())
        except KeyboardInterrupt:
            self.logger.warning("Keyboard interrupt - exiting...")
            return
