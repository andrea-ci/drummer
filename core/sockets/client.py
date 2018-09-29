import socket
from core.sockets.messages import Message

class SocketClientException(Exception):
    pass

class SocketClient():

    def init_socket(self):

        # Create TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = ('localhost', 10200)

        return sock, server_address


    def send(self, request):

        # init socket
        sock, server_address = self.init_socket()

        print('connecting to port {0}'.format(server_address))

        # get size of request
        req_size = str(len(request))

        # establish a connection
        try:
            sock.connect(server_address)

        except ConnectionRefusedError as e:
            raise SocketClientException('socket refused connection')

        except Exception:
            raise SocketClientException('connection error')

        try:

            # Send data size
            print('sending request size')

            res = sock.sendall(req_size.encode('utf-8'))

            if res:
                raise SocketClientException('cannot send request size to server')

            size_ack = sock.recv(4096)

            if size_ack:

                print('ack received: {0}'.format(size_ack.decode('utf-8')))

                # send message
                print('sending now request message')

                res = sock.sendall(request)

                if res:
                    raise SocketClientException('cannot send request message to server')

                response = self.get_response(sock)

            else:
                raise SocketClientException('impossible to send request to server')

        except Exception:
            raise SocketClientException('generic error, impossible to send request')

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


if __name__ == '__main__':

    #request = Request.encode('ciaociao', 'noargs')
    #request = 'ciao'.encode('utf-8')

    request = (
        Message()
        .add_entry('type', 'request')
        .add_entry('content', 'ciao ciao')
        .add_entry('exec_path', '/opt/sledge/tasks/remotedummy')
        .add_entry('parameters', 'verbose')
        .to_bytes()
    )

    sc = SocketClient()
    response = sc.send(request)

    print(Message.from_bytes(response))
