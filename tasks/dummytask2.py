#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.foundation.messages import Response, StatusCode
from datetime import datetime

class DummyTask2():

    def run(self, params):

        response = Response()

        try:

            # task logic
            dd = datetime.now()

            with open('dummy2.txt', 'a', encoding='utf-8') as f:
                f.write('I am the brother of dummy task\n')
                f.write('and I am running at {0}\n'.format(dd))

            # task response
            response.set_status(StatusCode.STATUS_OK)
            response.set_description('all right')

        except Exception:

            response.set_status(StatusCode.STATUS_ERROR)
            response.set_description('something was wrong')

        finally:
            return response
