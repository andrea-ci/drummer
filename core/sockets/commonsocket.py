#!/usr/bin/python3
# -*- coding: utf-8 -*-
from base import Configuration
from base import Message, MessageCode
import socket

class CommonSocketException(Exception):
    pass


class CommonSocket():

    def __init__(self):

        # Create TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # load configuration
        config = Configuration.load()
        socket_config = config.get('socket')

        hostname = socket_config.get('address')
        port = socket_config.get('port')

        server_address = (hostname, port)

        max_connections = socket_config.get('max_connections')
        MSG_LEN = socket_config.get('message_len')

        # set socket objects
        self.server_address = server_address
        self.max_connections = max_connections
        self.MSG_LEN = MSG_LEN


    def ask_handshake(self, message):

        sock = self.sock
        buffer_size = self.buffer_size

        msg_size = str(len(message))
        print('sending msg size {0}'.format(msg_size))

        try:

            # send message size
            res = sock.sendall(msg_size.encode('utf-8'))

            if res:
                raise CommonSocketException('cannot send message size to server')

            # wait for answer
            size_ack = sock.recv(buffer_size)

        except:
            raise CommonSocketException('cannot start handshake')

        return size_ack


    def serve_handshake(self, connection):

        buffer_size = self.buffer_size

        try:

            # wait for handshake
            data_size = connection.recv(buffer_size).decode('utf-8')
            #print('received {0}'.format(data_size))

            # send response about message size
            connection.send(MessageCode.STATUS_OK.encode('utf-8'))

        except:
            raise CommonSocketException('cannot complete handshake')

        return data_size


    def receive_data(self, connection):

        MSG_LEN = self.MSG_LEN

        data = b''
        bytes_received = 0

        while bytes_received < MSG_LEN:

            chunk = connection.recv(MSG_LEN)

            bytes_received += len(chunk)

            if chunk == b'':
                raise CommonSocketException('socket breakdown')

            data += chunk

        return data
