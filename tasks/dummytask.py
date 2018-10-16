#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.foundation import Response, StatusCode
from datetime import datetime

class DummyTask():

    def run(self, params):

        response = Response()

        try:

            # task logic
            dd = datetime.now()

            with open('dummy.txt', 'a', encoding='utf-8') as f:
                f.write('I am just a dummy task\n')
                f.write('and I am running at {0}\n'.format(dd))

            # task response
            response.set_status(StatusCode.STATUS_OK)
            response.set_description('all right')

        except Exception:

            response.set_status(StatusCode.STATUS_ERROR)
            response.set_description('something was wrong')

        finally:
            return response
