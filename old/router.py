#!/usr/bin/python3
# -*- coding: utf-8 -*-

class RouterException(Exception):
    pass


class Router():

    def perform_request(self, request):

        # local request
        if request.body.get('execution') == 'local':
            response = self.call_local_execution(request)

        # remote request
        elif request.body.get('execution') == 'remote':
            response = self.call_remote_execution(request)

        else:
            raise RouterException('unknown execution type for the request')


    def call_local_execution(self, request):
        print('local execution')


    def call_remote_execution(self, request):
        print('remote execution')
