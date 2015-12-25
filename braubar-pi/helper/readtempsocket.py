import asyncio

class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))

class ReadTempSocket:
    loop = None
    server = None

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        # Each client connection will create a new protocol instance
        coro = self.loop.create_server(EchoServerClientProtocol, '192.168.2.9', 8081)
        self.server = self.loop.run_until_complete(coro)

    def run(self):
        # Serve requests until Ctrl+C is pressed
        print('Serving on {}'.format(self.server.sockets[0].getsockname()))
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        self.exit()

    def exit(self):
        # Close the server
        self.server.close()
        self.loop.run_until_complete(self.server.wait_closed())
        self.loop.close()




