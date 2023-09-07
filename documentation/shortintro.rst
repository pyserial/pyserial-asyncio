========
Overview
========

Serial transports, protocols and streams
----------------------------------------

This module layers `asyncio <https://docs.python.org/3/library/asyncio.html>`_ support onto
`pySerial <http://pyserial.readthedocs.io/>`_. It provides support for working with serial
ports through *asyncio*
`Transports <https://docs.python.org/3/library/asyncio-protocol.html#transports>`_,
`Protocols <https://docs.python.org/3/library/asyncio-protocol.html#protocols>`_, and
`Streams <https://docs.python.org/3/library/asyncio-stream.html>`_.

Transports are a low-level abstraction, provided by this package in the form of an
:class:`asyncio.Transport` implementation called :class:`SerialTransport`, which manages the
asynchronous transmission of data through an underlying *pySerial* :class:`~serial.Serial`
instance. Transports are concerned with *how* bytes are transmitted through the serial port.

Protocols are a callback-based abstraction which determine *which* bytes are transmitted
through an underlying transport. You can implement a subclass of :class:`asyncio.Protocol` which
reads from, and/or writes to, a :class:`~serial_asyncio_fast.SerialTransport`. When a serial connection
is established your protocol will be handed a transport, to which your protocol
implementation can write data as necessary. Incoming data and other serial connection lifecycle
events cause callbacks on your protocol to be invoked, so it can take action as necessary.

Usually, you will not create a :class:`~serial_asyncio_fast.SerialTransport` directly. Rather, you will
define a ``Protocol`` class and pass that protocol to a function such as
:func:`~serial_asyncio_fast.create_serial_connection()` which will instantiate your ``Protocol`` and
connect it to a :class:`~serial_asyncio_fast.SerialTransport`.

Streams are a coroutine-based alternative to callback-based protocols. This package provides a
function :func:`~serial_asyncio_fast.open_serial_connection` which returns :class:`asyncio.StreamReader`
and :class:`asyncio.StreamWriter` objects for interacting with underlying protocol and transport
objects, which this library will create for you.


Protocol Example
----------------

This example defines a very simple Protocol which sends a greeting message through the serial port
and displays to the console any data received through the serial port, until a newline byte is
received.

A call is made to :func:`create_serial_connection()`, to which the protocol *class* (not an
instance) is passed, together with arguments destined for the :class:`~serial.Serial` constructor.
This call returns a coroutine object. When passed to :func:`~asyncio.run_until_complete` the
coroutine is scheduled to run as an :class:`asyncio.Task` by the *asyncio* library, and the result
of the coroutine, which is a tuple containing the transport and protocol instances, return to the
caller.

While the event loop is running (:meth:`~asyncio.AbstractEventLoop.loop.run_forever`), or until
the protocol closes the transport itself, the protocol will process data received through the serial
port asynchronously::


    import asyncio
    import serial_asyncio_fast

    class OutputProtocol(asyncio.Protocol):
        def connection_made(self, transport):
            self.transport = transport
            print('port opened', transport)
            transport.serial.rts = False  # You can manipulate Serial object via transport
            transport.write(b'Hello, World!\n')  # Write serial data via transport

        def data_received(self, data):
            print('data received', repr(data))
            if b'\n' in data:
                self.transport.close()

        def connection_lost(self, exc):
            print('port closed')
            self.transport.loop.stop()

        def pause_writing(self):
            print('pause writing')
            print(self.transport.get_write_buffer_size())

        def resume_writing(self):
            print(self.transport.get_write_buffer_size())
            print('resume writing')

    loop = asyncio.get_event_loop()
    coro = serial_asyncio_fast.create_serial_connection(loop, OutputProtocol, '/dev/ttyUSB0', baudrate=115200)
    transport, protocol = loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()

Reading data in chunks
----------------------

This example will read chunks from the serial port every 300ms::


    import asyncio
    import serial_asyncio_fast
    
    
    class InputChunkProtocol(asyncio.Protocol):
        def connection_made(self, transport):
            self.transport = transport
        
        def data_received(self, data):
            print('data received', repr(data))
            
            # stop callbacks again immediately
            self.pause_reading()
                
        def pause_reading(self):
            # This will stop the callbacks to data_received
            self.transport.pause_reading()
                
        def resume_reading(self):
            # This will start the callbacks to data_received again with all data that has been received in the meantime.
            self.transport.resume_reading()
        
    
    async def reader():
        transport, protocol = await serial_asyncio_fast.create_serial_connection(loop, InputChunkProtocol, '/dev/ttyUSB0', baudrate=115200)
    
        while True:
            await asyncio.sleep(0.3)
            protocol.resume_reading()
    
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(reader())
    loop.close()
