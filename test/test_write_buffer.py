# This file is part of pySerial-asyncio.
# SPDX-License-Identifier: BSD-3-Clause
import asyncio
import os
import unittest

if os.name == 'posix':
    import pty
    import fcntl

import serial_asyncio


@unittest.skipUnless(os.name == 'posix', 'requires a POSIX pseudo-terminal')
class TestWriteBuffer(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        self.master, self.slave = pty.openpty()
        flags = fcntl.fcntl(self.master, fcntl.F_GETFL)
        fcntl.fcntl(self.master, fcntl.F_SETFL, flags | os.O_NONBLOCK)
        self.errors = []
        self.loop.set_exception_handler(lambda loop, context: self.errors.append(context))
        self.closed = self.loop.create_future()
        closed = self.closed

        class Protocol(asyncio.Protocol):
            def connection_lost(self, exc):
                if not closed.done():
                    closed.set_result(exc)

        self.transport, _ = self.loop.run_until_complete(
            serial_asyncio.create_serial_connection(
                self.loop, Protocol, os.ttyname(self.slave)))

    def tearDown(self):
        try:
            self.transport.abort()
            self.loop.run_until_complete(asyncio.wait_for(self.closed, 2))
            self.loop.run_until_complete(asyncio.sleep(0))
        finally:
            os.close(self.master)
            os.close(self.slave)
            self.loop.close()

    async def receive(self, length):
        received = b''
        while len(received) < length:
            try:
                received += os.read(self.master, length - len(received))
            except BlockingIOError:
                await asyncio.sleep(0.01)
        return received

    def assertWritten(self, expected):
        received = self.loop.run_until_complete(
            asyncio.wait_for(self.receive(len(expected)), 2))
        self.assertEqual(received, expected)
        self.assertEqual(self.errors, [])

    def test_bytearray_can_be_cleared_after_write(self):
        data = bytearray(b'command')
        self.transport.write(data)
        data.clear()
        self.assertWritten(b'command')

    def test_memoryview_can_be_changed_after_write(self):
        data = bytearray(b'command')
        self.transport.write(memoryview(data))
        data[:] = b'changed'
        self.assertWritten(b'command')

    def test_empty_write_then_normal_write(self):
        for data in (b'', bytearray(), memoryview(b'')):
            self.transport.write(data)
            self.loop.run_until_complete(asyncio.sleep(0.02))
        self.assertEqual(self.errors, [])
        self.transport.write(b'command')
        self.assertWritten(b'command')

    def test_multiple_writes_keep_order(self):
        for data in (b'one', bytearray(b'two'), memoryview(b'three')):
            self.transport.write(data)
        self.assertWritten(b'onetwothree')

    def test_non_buffer_argument_is_rejected(self):
        with self.assertRaises(TypeError):
            self.transport.write(7)
        self.transport.write(b'command')
        self.assertWritten(b'command')
