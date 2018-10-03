#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.sockets.commonsocket import CommonSocket
from base import Message, MessageCode

# accepted connections
class SocketServerException(Exception):
    pass


class SocketServer(CommonSocket):

    def __init__(self, conn):

        super().__init__()

        self.conn_s2m = conn


    def run(self):

        sock = self.sock
        server_address = self.server_address
        max_connections = self.max_connections
        MSG_LEN = self.MSG_LEN

        # bind socket
        sock.bind(server_address)

        # listen mode
        sock.listen(max_connections)

        while True:

            # open a new connection
            connection, client_address = sock.accept()

            with connection:

                try:

                    # handle data handshake
                    #data_size = self.serve_handshake(connection)

                    # get data from client
                    data = self.receive_data(connection)

                    # decode client request
                    request = Message.from_bytes(data)

                    # send request to master
                    self.conn_s2m.send(request)

                    



                    # send response to client
                    response = Message()
                    response.add_entry('type', 'response')
                    response.add_entry('status', MessageCode.STATUS_OK)
                    data = response.to_bytes(MSG_LEN)

                    # start size handshake
                    #size_ack = self.ask_handshake(response)

                    #connection = self.send_response(connection, received_data)
                    res = connection.sendall(data)

                except Exception:
                    raise SocketServerException('error in server socket')

                finally:

                    # Clean up the connection
                    #connection = self.send_response(connection)
                    connection.close()
