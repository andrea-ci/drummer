#!/usr/bin/python3
# -*- coding: utf-8 -*-
from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCServer
from core.daemon import Daemon

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class SocketServer(Daemon):

    def run(self):


        #configuration = Configuration.load()
        #socket_data = configuration.get('server-socket').split(':')
        #hostname = socket_data[0]
        #port = int(socket_data[1])
        hostname = 'localhost'
        port = 10200

        server = SimpleXMLRPCServer((hostname,port), requestHandler=RequestHandler)

        server.register_introspection_functions()

        # Register pow() function; this will use the value of
        # pow.__name__ as the name, which is just 'pow'.
        server.register_function(pow)

        # Register a function under a different name
        def adder_function(x, y):
            return x + y
        server.register_function(adder_function, 'add')

        # Register an instance; all the methods of the instance are
        # published as XML-RPC methods (in this case, just 'mul').
        class MyFuncs:
            def mul(self, x, y):
                return x * y

        server.register_instance(MyFuncs())

        # Run the server's main loop
        server.serve_forever()
