#!/usr/bin/env python
#
# This file is part of pySerial-asyncio - Cross platform serial port support for Python
# (C) 2016 pySerial-team
#
# SPDX-License-Identifier:    BSD-3-Clause
"""\
Test asyncio related functionality.

To run from the command line with a specific port with a loop-back,
device connected, use:

  $ cd pyserial-asyncio
  $ python -m test.test_asyncio SERIALDEVICE

"""

import os
import unittest
import asyncio
from typing import Optional

import serial_asyncio_fast

HOST = "127.0.0.1"
_PORT = 8888

# on which port should the tests be performed:
PORT = "socket://%s:%s" % (HOST, _PORT)


@unittest.skipIf(os.name != "posix", "asyncio not supported on platform")
class Test_asyncio(unittest.TestCase):
    """Test asyncio related functionality"""

    def setUp(self):
        self.loop = asyncio.get_event_loop()
        # create a closed serial port

    def tearDown(self):
        self.loop.close()

    def test_asyncio(self):
        TEXT = b"Hello, World!"
        COUNT = 1024
        COMPLETE_MESSAGE = TEXT * COUNT + b"\n"
        received = []
        actions = []
        done = asyncio.Event()

        class Input(asyncio.Protocol):
            def __init__(self):
                super().__init__()
                self._transport = None

            def connection_made(self, transport: serial_asyncio_fast.SerialTransport):
                self._transport = transport

            def data_received(self, data):
                self._transport.write(data)

        class Output(asyncio.Protocol):
            def __init__(self):
                super().__init__()
                self._transport: Optional[serial_asyncio_fast.SerialTransport] = None

            def connection_made(self, transport: serial_asyncio_fast.SerialTransport):
                self._transport = transport
                actions.append("open")
                for _ in range(COUNT):
                    transport.write(TEXT)
                transport.write(b"\n")

            def data_received(self, data):
                received.append(data)
                if b"\n" in data:
                    self._transport.close()

            def connection_lost(self, exc):
                actions.append("close")
                done.set()

            def pause_writing(self):
                actions.append("pause")
                print(self._transport.get_write_buffer_size())

            def resume_writing(self):
                actions.append("resume")
                print(self._transport.get_write_buffer_size())

        if PORT.startswith("socket://"):
            coro = self.loop.create_server(Input, HOST, _PORT)
            self.loop.run_until_complete(coro)

        client = serial_asyncio_fast.create_serial_connection(self.loop, Output, PORT)
        self.loop.run_until_complete(client)
        self.loop.run_until_complete(done.wait())
        pending = asyncio.all_tasks(self.loop)
        self.loop.run_until_complete(asyncio.gather(*pending))
        for _ in range(1024):
            self.loop.run_until_complete(asyncio.sleep(0))
        all_data = b"".join(received)
        self.assertEqual(all_data, COMPLETE_MESSAGE)
        self.assertEqual(actions, ["open", "close"])


if __name__ == "__main__":
    import sys

    sys.stdout.write(__doc__)
    if len(sys.argv) > 1:
        PORT = sys.argv[1]
    sys.stdout.write("Testing port: %r\n" % PORT)
    sys.argv[1:] = ["-v"]
    # When this module is executed from the command-line, it runs all its tests
    unittest.main()
