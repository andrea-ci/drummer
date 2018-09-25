#!/usr/bin/python3
# -*- coding: utf-8 -*-
from multiprocessing import Process
import socket
#from ipc.server import SocketServer

class Listener(Process):
    """ this worker starts socket server with a pipe to communicate with master """

    def __init__(self, conn):

        super().__init__()

        self.conn = conn


    def run(self):

        # run socket server
        #server = SocketServer(self.conn)
        #server.run()
        sock, max_connections, buffer_size = self.create_socket()

        # listen mode
        sock.listen(max_connections)

        while True:

            connection, client_address = sock.accept()

            try:

                print('connection from {0}'.format(client_address))

                # Receive the data in small chunks and retransmit it
                while True:

                    data = connection.recv(buffer_size).decode('utf-8')

                    print('received {0}'.format(data))

                    if data:

                        print('sending data back to the client')

                        connection.sendall(data.encode('utf-8'))

                    else:
                        print('no more data from {0}'.format(client_address))
                        break

            finally:

                # Clean up the connection
                connection.close()


    def create_socket(self):

        config = Configuration.load()
        socket_config = config.get('socket')

        hostname = socket_config.get('address')
        port = socket_config.get('port')

        max_connections = socket_config.get('max_connections')
        buffer_size = socket_config.get('buffer_size')

        # create TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # bind the socket
        sock.bind( (hostname, port) )

        return sock, max_connections, buffer_size
