======================
 pySerial-asyncio API
======================

asyncio
=======

.. module:: serial.aio

.. warning:: This implementation is currently in an experimental state. Use
    at your own risk.

Experimental asyncio support is available for Python 3.4 and newer. The module
:mod:`serial.aio` provides a :class:`asyncio.Transport`:
``SerialTransport``.


A factory function (`asyncio.coroutine`) is provided:

.. function:: create_serial_connection(loop, protocol_factory, \*args, \*\*kwargs)

    :param loop: The event handler
    :param protocol_factory: Factory function for a :class:`asyncio.Protocol`
    :param args: Passed to the :class:`serial.Serial` init function
    :param kwargs: Passed to the :class:`serial.Serial` init function
    :platform: Posix

    Get a connection making coroutine.

Example::

    class Output(asyncio.Protocol):
        def connection_made(self, transport):
            self.transport = transport
            print('port opened', transport)
            transport.serial.rts = False
            transport.write(b'hello world\n')

        def data_received(self, data):
            print('data received', repr(data))
            self.transport.close()

        def connection_lost(self, exc):
            print('port closed')
            asyncio.get_event_loop().stop()

    loop = asyncio.get_event_loop()
    coro = serial.aio.create_serial_connection(loop, Output, '/dev/ttyUSB0', baudrate=115200)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()

