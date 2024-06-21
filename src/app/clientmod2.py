import asyncio
import concurrent.futures
import json
import logging
import time
from typing import (
    Iterable,
    Optional
)

import requests
from colorama import Fore, Back, Style
import subprocess
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


class SignalRClientMod2:
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

    def __init__(self, WLED_GREEN: int, WLED_TRACKCLEAR: int, WLED_RED: int, WLED_YELLOW: int, WLED_CHEQUERED: int, WLED_SC: int, WLED_HOST: str = '', WLED_DELAY: int = 0, filemode: str = 'w', debug: bool = False,
                 timeout: int = 60, logger: Optional = None):

        self.headers = {'User-agent': 'BestHTTP',
                        'Accept-Encoding': 'gzip, identity',
                        'Connection': 'keep-alive, Upgrade'}

        """
        self.topics = ["Heartbeat", "CarData.z", "Position.z",
                       "ExtrapolatedClock", "TopThree", "RcmSeries",
                       "TimingStats", "TimingAppData",
                       "WeatherData", "TrackStatus", "DriverList",
                       "RaceControlMessages", "SessionInfo",
                       "SessionData", "LapCount", "TimingData"]
        """
        self.topics = ["Heartbeat", "RaceControlMessages"]
        self.WLED_GREEN = WLED_GREEN
        self.WLED_TRACKCLEAR = WLED_TRACKCLEAR
        #self.WLED_YELLOW = WLED_YELLOW
        self.WLED_RED = WLED_RED
        self.WLED_CHEQUERED = WLED_CHEQUERED
        self.WLED_SC = WLED_SC
        self.WLED_HOST = WLED_HOST
        self.WLED_DELAY = WLED_DELAY

        self.debug = debug
        self.filename = '/app/output.txt'
        self.filemode = 'w'
        self.timeout = timeout
        self._connection = None

        self.sector_status = {}
        self.current_status = ""

        if not logger:
            logging.basicConfig(
                format="%(asctime)s - %(levelname)s: %(message)s"
            )
            self.logger = logging.getLogger('SignalR')
            self.logger.setLevel(logging.INFO)
        else:
            self.logger = logger

        self._output_file = open(self.filename, self.filemode)
        self._t_last_message = None

    def _to_file(self, msg):
        self._output_file.write(msg + '\n')
        self._output_file.flush()

    def fix_json(self, msg):
        msg = msg.replace("'", '"') .replace('True', 'true').replace('False', 'false')
        return msg

    def to_wled(self, action):
        # action should be one of: GREEN, TRACKCLEAR, YELLOW, RED, CHEQUERED, SC
        if action == 'GREEN':
            preset = self.WLED_GREEN
        elif action == 'TRACKCLEAR':
            preset = self.WLED_TRACKCLEAR
        elif action == 'YELLOW':
            preset = self.WLED_YELLOW
        elif action == 'RED':
            preset = self.WLED_RED
        elif action == 'CHEQUERED':
            preset = self.WLED_CHEQUERED
        elif action == 'SC':
            preset = self.WLED_SC
        else:
            return

        url = "http://" + self.WLED_HOST + "/win&PL=" + str(preset)
        print(Fore.GREEN, url, Fore.RESET)
        "Called " + url + " with " + str(self.WLED_DELAY) + " delay"
        #response = requests.get(url, timeout=1)
        #print(response.status_code)
        command = "nohup /app/cmd.sh '" + url + "' " + str(self.WLED_DELAY) + " > /dev/null 2>&1 &"
        null = subprocess.Popen(command, shell=True)

    def handle_message(self, msg):
        try:
            self._output_file.write(msg + '\n')
            self._output_file.flush()
        except Exception as e:
            print(f"Error writing to file: {e}")

        #Fix and load json
        msg = self.fix_json(msg)
        print(Fore.CYAN, msg, Fore.RESET)
        msg = json.loads(msg)
        
        if 'R' in msg:
            self.handle_replay(msg)
        else:
            activities = list()

            if 'M' in msg and len(msg['M']) > 0:
                for m in msg['M']:
                    if 'A' in m:
                        activities.append(m['A'])
            else:
                activities.append(msg)
            
            for activity in activities:
                if 'RaceControlMessages' in activity:
                    messages = activity[1]['Messages']
                else:
                    messages = {}

                for m in messages:
                    message = messages[m]
                    # Message should be something like: {'Utc': '2024-05-18T15:01:42', 'Category': 'Other', 'Message': 'FIA STEWARDS: Q1 INCIDENT INVOLVING CARS 24 (ZHO), 1 (VER), 11 (PER), 55 (SAI), 10 (GAS), 16 (LEC), 2 (SAR), 3 (RIC) NO FURTHER ACTION - FAILING TO FOLLOW RACE DIRECTORS INSTRUCTIONS - MAXIMUM DELTA TIME'}
                    action = ''

                    if message['Category'] == 'Flag':
                        if message['Flag'] == 'GREEN':
                            print(Fore.GREEN + "Green Flag" + Fore.RESET + " " + message['Message'])
                            action = 'GREEN'
                        elif message['Flag'] == 'YELLOW' or message['Flag'] == 'DOUBLE YELLOW':
                            print(Fore.YELLOW + "Yellow Flag" + Fore.RESET + " " + message['Message'])
                            action = '' # Do nothing for yellow flags.
                            if message['Scope'] == 'Sector':
                                self.sector_status[message['Sector']] = 'YELLOW'
                                if self.current_status != 'RED' and self.current_status != 'SC':
                                    action = 'YELLOW'
                        elif message['Flag'] == 'RED':
                            print(Fore.RED + "Red Flag" + Fore.RESET)
                            action = 'RED'
                            self.sector_status = {'Track': 'RED'}
                            self.current_status = 'RED'
                        elif message['Flag'] == 'CLEAR':
                            if message['Scope'] == 'Track': # Track Clear.
                                print(Fore.CYAN + "Clear Flag" + Fore.RESET + " " + message['Message'])
                                self.sector_status = {'Track': 'TRACKCLEAR'}
                                self.current_status = 'TRACKCLEAR'
                                action = 'TRACKCLEAR'
                            else: # Clear flag for a sector. 
                                self.sector_status[message['Sector']] = 'CLEAR'
                                # Check if all sectors are clear.
                                #print(Back.CYAN + Fore.BLACK + message['Message'] + Fore.RESET + Back.RESET)
                                action = 'TRACKCLEAR'
                                for sector in self.sector_status:
                                    if self.sector_status[sector] == 'YELLOW':
                                        action = 'YELLOW'
                                        break
                                if self.current_status != 'RED' and self.current_status != 'SC' and action == 'TRACKCLEAR':
                                    action = 'TRACKCLEAR'
                                else:
                                    action = ''
                        elif message['Flag'] == 'CHEQUERED':
                            print(Fore.MAGENTA + "Chequered Flag" + Fore.RESET + " " + message['Message'])
                            action = 'CHEQUERED'
                            self.track_status = {'Track': 'CHEQUERED'}
                        else:
                            print(Fore.MAGENTA + message['Message'] + Fore.RESET)
                    elif message['Category'] == 'SafetyCar':
                        print(Back.YELLOW + "Safety Car" + Back.RESET + " " + message['Message'])
                        action = 'SC'
                        self.current_status = 'SC'
                    
                    if action != '':
                        self.to_wled(action)

    def handle_replay(self, replay):
        #TODO: Implement replay functionality
        self.sector_status = {}
        action = ''

        if 'R' in replay:
            if 'RaceControlMessages' in replay['R']:
                 # Handle messages
                 messages = replay['R']['RaceControlMessages']['Messages']
                 for message in messages:
                    if message['Category'] == 'Flag':
                        if message['Flag'] == 'YELLOW' or message['Flag'] == 'DOUBLE YELLOW':
                            if message['Scope'] == 'Sector':
                                self.sector_status[message['Sector']] = 'YELLOW'
                            elif message['Scope'] == 'Track':
                                self.sector_status['Track'] = 'YELLOW'
                        elif message['Flag'] == 'CLEAR':
                            if message['Scope'] == 'Sector':
                                self.sector_status[message['Sector']] = 'CLEAR'
                            elif message['Scope'] == 'Track':
                                self.sector_status = {'Track': 'TRACKCLEAR'}
                                self.current_status = 'TRACKCLEAR'
                        elif message['Flag'] == 'GREEN':
                            self.sector_status = {'Track': 'GREEN'}
                        elif message['Flag'] == 'RED':
                            self.sector_status = {'Track': 'RED'}
                            self.current_status = 'RED'
                        elif message['Flag'] == 'CHEQUERED':
                            self.sector_status = {'Track': 'CHEQUERED'}
                    elif message['Category'] == 'SafetyCar':
                        if message['Status'] == 'DEPLOYED':
                            self.current_status = 'SC'

            if self.current_status != 'RED' and self.current_status != 'SC':
                if 'Track' in self.sector_status and len(self.sector_status) == 1:
                        # Only track status
                        action = self.sector_status['Track']
                else:
                    action = 'TRACKCLEAR'
                    for sector in self.sector_status:
                        if self.sector_status[sector] == 'YELLOW':
                            action = 'YELLOW'
                            break
            else: # Safety car or red flag trumps yellow flags.
                action = self.current_status
            
            if action != '':
                self.to_wled(action)

    async def _on_do_nothing(self, msg):
        # just do nothing with the message; intended for debug mode where some
        # callback method still needs to be provided
        pass

    async def _on_message(self, msg):
        self._t_last_message = time.time()
        loop = asyncio.get_running_loop()
        try:
            with concurrent.futures.ThreadPoolExecutor() as pool:
                await loop.run_in_executor(
                    pool, self.handle_message, str(msg)
                )
        except Exception:
            self.logger.exception("Exception while writing message to file")

    async def _on_debug(self, **data):
        if 'M' in data and len(data['M']) > 0:
            self._t_last_message = time.time()

        loop = asyncio.get_running_loop()
        try:
            with concurrent.futures.ThreadPoolExecutor() as pool:
                await loop.run_in_executor(
                    pool, self.handle_message, str(data)
                )
        except Exception:
            self.logger.exception("Exception while writing message to file")

    async def _run(self):
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
                while self._connection.started:
                    await asyncio.sleep(0.1)
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
            # try to get an already running loop (e.g. in newer IPython)
            loop = asyncio.get_running_loop()
        except RuntimeError:
            # there is no running loop yet
            self._start_without_existing_loop()
            return

        try:
            __IPYTHON__  # noqa
            is_ipython = True
        except NameError:
            is_ipython = False

        if loop and is_ipython:
            raise RuntimeError(
                "Running in an asynchronous IPython session. "
                "Please use `await SignalRClient().async_start()`"
            )

        else:
            raise RuntimeError(
                "Cannot start because an asynchronous event loop already "
                "exists. You can try to use the "
                "`SignalRClient().async_start()` coroutine."
            )

    async def async_start(self):
        """
        Connect to the data stream and start writing the data to a file
        when running inside an existing event loop.

        In most cases, you want to use :func:`start` instead.
        """
        loop = asyncio.get_running_loop()
        try:
            task = loop.create_task(self._async_start())
            while not task.done():
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            self.logger.warning("Async execution cancelled - exiting...")

    def _start_without_existing_loop(self):
        try:
            asyncio.run(self._async_start())
        except KeyboardInterrupt:
            self.logger.warning("Keyboard interrupt - exiting...")