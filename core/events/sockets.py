#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.foundation.messages import Response, StatusCode

class SocketTest:
    """ simple event to check socket connection """

    def execute(self, request):

        response = Response()

        try:
            response.set_status(StatusCode.STATUS_OK)

        except Exception:
            response.set_status(StatusCode.STATUS_ERROR)

        return response
