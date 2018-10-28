#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.sockets.commonsocket import CommonSocket
from core.foundation import ByteMessage, Response, StatusCode

# accepted connections
class SocketServerException(Exception):
    pass


class SocketServer(CommonSocket):

    def __init__(self, queue_w2m, queue_m2w):

        super().__init__()

        self.queue_w2m = queue_w2m
        self.queue_m2w = queue_m2w
        
    def run(self):

        sock = self.sock
        server_address = self.server_address
        max_connections = self.max_connections
        MSG_LEN = self.MSG_LEN

        bytemessage = ByteMessage(MSG_LEN)

        # bind socket
        sock.bind(server_address)

        # listen mode
        sock.listen(max_connections)

        while True:

            # open a new connection
            connection, client_address = sock.accept()

            with connection:

                try:

                    # get data from client
                    encoded_request = self.receive_data(connection)

                    # decode client request
                    request = bytemessage.decode(encoded_request)

                    # send request to master
                    self.queue_w2m.put(request)

                    # wait for response
                    response = self.queue_m2w.get(block=True, timeout=None)

                    # send response to client
                    encoded_response = bytemessage.encode(response)
                    res = connection.sendall(encoded_response)

                except Exception:
                    raise SocketServerException('error in server socket')

                finally:
                    # Clean up the connection
                    connection.close()
