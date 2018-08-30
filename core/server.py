#!/usr/bin/python3
# -*- coding: utf-8 -*-
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class SocketServer(SimpleXMLRPCServer):

    def __init__(self, configuration):

        socket_data = configuration.get('server-socket').split(':')

        hostname = socket_data[0]
        port = int(socket_data[1])

        super().__init__((hostname,port), requestHandler=RequestHandler)
