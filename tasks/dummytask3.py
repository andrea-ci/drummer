#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.foundation.messages import Response, StatusCode
from datetime import datetime
from time import sleep

class DummyTask3:

    def run(self, params):

        response = Response()

        try:

            while True:

                # task logic
                dd = datetime.now()

                with open('dummy.txt', 'a', encoding='utf-8') as f:
                    f.write('I am a never ending task\n')
                    f.write('and I am running at {0}\n'.format(dd))

                sleep(120)

            # task response
            response.set_status(StatusCode.STATUS_OK)
            response.set_data({'Description': 'all right'})

        except Exception:

            response.set_status(StatusCode.STATUS_ERROR)
            response.set_data({'Description': 'something was wrong'})

        finally:
            return response
