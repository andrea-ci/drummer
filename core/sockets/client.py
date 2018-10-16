#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.foundation import ByteMessage
from core.sockets.commonsocket import CommonSocket


class SocketClientException(Exception):
    pass


class SocketClient(CommonSocket):

    def check_connection(self):

        connected = False

        sock = self.sock
        server_address = self.server_address

        # establish a connection
        try:
            sock.connect(server_address)

        except ConnectionRefusedError as e:
            raise SocketClientException('socket refused connection')

        except Exception:
            raise SocketClientException('connection error')

        else:
            connected = True

        finally:
            # close connection
            sock.close()

        return connected


    def send_request(self, request):

        # init socket
        sock = self.sock
        server_address = self.server_address
        MSG_LEN = self.MSG_LEN

        bytemessage = ByteMessage(MSG_LEN)

        # establish a connection
        try:
            sock.connect(server_address)

        except ConnectionRefusedError as e:
            raise SocketClientException('socket refused connection')

        except Exception:
            raise SocketClientException('connection error')

        try:

            # encode and send request
            request = bytemessage.encode(request)
            res = sock.sendall(request)

            if res:
                raise SocketClientException('cannot send request message to server')

            # get data from server and decode
            response = self.receive_data(sock)
            response = bytemessage.decode(response)

        except:
            raise SocketClientException('impossible to send request to server')

        finally:
            # close connection
            sock.close()

        return response


    def get_response(self, sock):

        response = b''

        receiving = True
        while receiving:

            new_data = sock.recv(4096)

            if new_data:
                response += new_data

            else:
                receiving = False

        return response
