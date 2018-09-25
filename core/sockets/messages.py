#!/usr/bin/python3
# -*- coding: utf-8 -*-
from datetime import datetime
import pickle

class MessageCode():

    STATUS_OK = 'ok'
    STATUS_WARNING = 'warning'
    STATUS_ERROR = 'error'


class Message():

    def __init__(self):
        self.data = dict()

    def add_entry(self, key, value):

        self.data[key] = value

        return self

    def to_bytes(self):

        s = ''
        for key, value in self.data.items():
            s += '{0}={1}&'.format(key, value)

        if s[-1] == '&':
            s = s[:-1]

        return s.encode('utf-8')

    @staticmethod
    def from_bytes(msg_bytes):

        d = dict()

        msg_str = msg_bytes.decode('utf-8')

        tuples = msg_str.split('&')

        for t in tuples:

            k, v = t.split('=')
            d[k] = v

        return d


class Request():

    @staticmethod
    def encode(exec_path, parameters):

        request = dict()
        request['exec_path'] = exec_path
        request['parameters'] = parameters

        return pickle.dumps(request)


    @staticmethod
    def decode(pickled):

        request = pickle.loads(pickled)

        return request


class Response():

    @staticmethod
    def encode(status_code, message):

        request = dict()
        request['status_code'] = status_code
        request['message'] = message

        return pickle.dumps(request)


    @staticmethod
    def decode(pickled):

        request = pickle.loads(pickled)

        return request
