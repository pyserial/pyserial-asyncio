====================
 Short introduction
====================

Example::

    class Output(asyncio.Protocol):
        def connection_made(self, transport):
            self.transport = transport
            print('port opened', transport)
            transport.serial.rts = False
            transport.write(b'hello world\n')

        def data_received(self, data):
            print('data received', repr(data))
            if b'\n' in data:
                self.transport.close()

        def connection_lost(self, exc):
            print('port closed')
            asyncio.get_event_loop().stop()

        def pause_writing(self):
            print('pause writing')
            print(self.transport.get_write_buffer_size())

        def resume_writing(self):
            print(self.transport.get_write_buffer_size())
            print('resume writing')

    loop = asyncio.get_event_loop()
    coro = create_serial_connection(loop, Output, '/dev/ttyUSB0', baudrate=115200)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()
