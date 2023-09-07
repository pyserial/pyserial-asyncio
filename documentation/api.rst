======================
 pySerial-asyncio API
======================

.. module:: serial_asyncio_fast


The following high-level functions are provided for initiating a serial connection:

.. function:: create_serial_connection(loop, protocol_factory, *args, **kwargs)
    :async:

    Open a streaming connection to the specified serial port.

    :param loop: The *asyncio* event loop
    :param protocol_factory: A callable which when invoked without arguments and which should
        return a :class:`asyncio.Protocol` subclass. Most commonly the protocol *class*
        (*e.g.* ``MyProtocol``) can be passed as this argument. If it is required to use an
        existing protocol *instance*, pass a zero-argument lambda which evaluates to the instance,
        such as ``lambda: my_protocol``
    :param args: Forwarded to the :class:`serial.Serial` constructor
    :param kwargs: Forwarded to the :class:`serial.Serial` constructor
    :returns: A coroutine for managing a serial port connection, which when
        awaited returns transport and protocol instances.
    :platform: Posix

    Use this function to associate an asynchronous call-back based protocol with an
    new :class:`serial.Serial` instance that will be created on your behalf.

    The chronological order of the operation is:

    1. ``protocol_factory`` is called without arguments and must return
       a :class:`asyncio.Protocol` subclass instance.

    2. The protocol instance is tied to a :class:`~serial_asyncio_fast.SerialTransport`.

    3. This coroutine returns successfully with a ``(transport, protocol)`` pair.

    4. The :meth:`~serial_asyncio_fast.SerialTransport.connection_made()` method of the protocol
       will be called at some point by the event loop.



.. function:: connection_for_serial(loop, protocol_factory, serial_instance)
    :async:

    Open a streaming connection to an existing serial port instance.

    :param loop: The *asyncio* event loop
    :param protocol_factory: A callable which when invoked without arguments and which should
        return a :class:`asyncio.Protocol` subclass. Most commonly the protocol *class*
        (*e.g.* ``MyProtocol``) can be passed as this argument. If it is required to use an
        existing protocol *instance*, pass a zero-argument lambda which evaluates to the instance,
        such as ``lambda: my_protocol``
    :param serial_instance: A :class:`serial.Serial` instance.
    :returns: A coroutine for managing a serial port connection, which when
        awaited returns transport and protocol instances.
    :platform: Posix

    Use this function to associate an asynchronous call-back based protocol with an
    existing :class:`serial.Serial` instance.

    The chronological order of the operation is:

    1. ``protocol_factory`` is called without arguments and must return
       a :class:`asyncio.Protocol` subclass instance.

    2. The protocol instance is tied to a :class:`~serial_asyncio_fast.SerialTransport`.

    3. This coroutine returns successfully with a ``(transport, protocol)`` pair.

    4. The :meth:`~serial_asyncio_fast.SerialTransport.connection_made()` method of the protocol
       will be called at some point by the event loop.


.. function:: open_serial_connection(*, loop=None, limit=None, **kwargs)
    :async:

    Open a streaming connection to an existing serial port instance.

    :param loop: The *asyncio* event loop
    :param limit: A optional buffer limit in bytes for the :class:`asyncio.StreamReader`
    :param kwargs: Forwarded to the :class:`serial.Serial` constructor
    :returns: A coroutine for managing a serial port connection, which when
        awaited returns an :class:`asyncio.StreamReader` and a :class:`asyncio.StreamWriter`.
    :platform: Posix

    Use this function to open connections where serial traffic is handled by
    an asynchronous coroutine interacting with :class:`asyncio.StreamReader` and a :class:`asyncio.StreamWriter` objects.
