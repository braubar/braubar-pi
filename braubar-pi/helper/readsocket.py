import os
import socket
import struct
import sys

import time


class ReadSocket:
    sock = None

    def __init__(self, ip, port):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        server_address = (ip, port)
        self.sock.bind(server_address)
        # Listen for incoming connections
        self.sock.listen(1)

    def read(self):
        result = None
        try:
            while True:

                # Wait for a connection
                print('waiting for a connection...')
                connection, client_address = self.sock.accept()
                print('connection from %s:%d' % client_address)
                try:
                    while True:
                        # Receive the data one byte at a time
                        data = connection.recv(6)
                        if data:
                            # Send back in uppercase
                            result = data
                            f = open("/tmp/braubar.temp", mode='ab')
                            f.write(result + bytes(os.linesep, 'utf-8'))
                            print(result)

                        else:
                            print('no more data, closing connection.')
                finally:
                    # Clean up the connection
                    connection.close()
        except KeyboardInterrupt:
            print('exiting.')
        finally:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
            time.sleep(1)


if __name__ == "__main__":
    ip = sys.argv[1]
    port = int(sys.argv[2])
    ReadSocket(ip, port).read()
