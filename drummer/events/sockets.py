#!/usr/bin/python3
# -*- coding: utf-8 -*-
from drummer.foundation.messages import Response, StatusCode, FollowUp

class SocketTestEvent:
    """ simple event to check socket connection """

    def execute(self, request):

        response = Response()

        follow_up = FollowUp(None)

        try:
            response.set_status(StatusCode.STATUS_OK)

        except Exception:
            response.set_status(StatusCode.STATUS_ERROR)

        return response, follow_up
