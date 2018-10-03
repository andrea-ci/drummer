#!/usr/bin/python3
# -*- coding: utf-8 -*-

class JobAdd():

    def execute(self, request):

        with open('dummy.txt', 'w') as f:

            for key in request:
                f.write('{0}: {1}\n'.format(key, request[key]))

        return
