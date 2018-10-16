#!/usr/bin/python3
# -*- coding: utf-8 -*-

class ResponseException(Exception):
    pass
class RequestException(Exception):
    pass


class StatusCode():
    STATUS_OK = 'ok'
    STATUS_WARNING = 'warning'
    STATUS_ERROR = 'error'


class MessageType():
    TYPE_REQUEST = 'request'
    TYPE_RESPONSE = 'response'
    TYPE_INFO = 'info'


class Info:
    """ Information message """
    def __init__(self):
        self.type = MessageType.TYPE_INFO
        self._content = ''
        self._sender = ''

    @property
    def content(self):
        return self._content

    @property
    def sender(self):
        return self._sender

    @content.setter
    def content(self, info):
        if isinstance(info, str):
            self._content = info
        else:
            raise RequestException('Information content must be a string')

    @sender.setter
    def sender(self, sender):
        if isinstance(sender, str):
            self._sender = sender
        else:
            raise RequestException('Sender must be a string')



class Request:
    """ Request object """
    def __init__(self):
        self.type = MessageType.TYPE_REQUEST
        self.classname = None
        self.classpath = None
        self.data = None

    def set_classname(self, classname):
        """ class to invoke for fulfilling the request """
        if isinstance(classname, str):
            self.classname = classname
        else:
            raise RequestException('Classname must be a string')

    def set_classpath(self, classpath):
        """ class to invoke for fulfilling the request """
        if isinstance(classpath, str):
            self.classpath = classpath
        else:
            raise RequestException('Classname must be a string')

    def set_data(self, data):
        """ data is a dict of param -> value """
        if isinstance(data, dict):
            self.data = data
        else:
            raise RequestException('Data of a request must be a dictionary')


class Response:
    """ Response object """
    def __init__(self):
        self.type = MessageType.TYPE_RESPONSE
        self.status = None
        self.description = None

    def set_status(self, status):
        """ set status code """
        if status not in (StatusCode.STATUS_OK, StatusCode.STATUS_WARNING, StatusCode.STATUS_ERROR):
            raise ResponseException('Status code not supported')
        self.status = status

    def set_description(self, description):
        """ set an optional message for the response """
        if isinstance(description, str):
            self.description = description
        else:
            raise ResponseException('Description must be a string')


class ByteMessage:
    def __init__(self, MSG_LEN):
        self.MSG_LEN = MSG_LEN

    def encode(self, message):
        """ encode a message to fixed-length byte array """

        if message.type == MessageType.TYPE_REQUEST:
            encoded = self.encode_request(message)
        elif message.type == MessageType.TYPE_RESPONSE:
            encoded = self.encode_response(message)
        elif message.type == MessageType.TYPE_INFO:
            encoded = self.encode_log(message)
        else:
            raise Exception('Message type not supported')
        return encoded

    def encode_request(self, message):

        s = 'type={0}&'.format(message.type)
        s += 'classname={0}&'.format(message.classname)
        s += 'classpath={0}&'.format(message.classpath)

        if message.data:
            for key, value in message.data.items():
                s += '{0}={1}&'.format(key, value)

        # convert to byets
        byte_data = s.encode('utf-8')
        # zero padding
        byte_data += b'0' * (self.MSG_LEN - len(byte_data))

        return byte_data

    def encode_response(self, message):

        s = 'type={0}&'.format(message.type)
        s += 'status={0}&'.format(message.status)

        if message.description:
            s += 'description={0}&'.format(message.description)

        # encode
        byte_data = s.encode('utf-8')

        # zero padding
        byte_data += b'0' * (self.MSG_LEN - len(byte_data))

        return byte_data

    def encode_log(self, message):
        pass

    def decode(self, message):
        """ decode message """

        # convert to string
        message = message.decode('utf-8')

        msg_parts = message.split('&')[:-1]

        # check message type
        msg_type = msg_parts[0].split('=')[1]

        if msg_type == MessageType.TYPE_REQUEST:
            decoded = self.decode_request(msg_parts)
        elif msg_type == MessageType.TYPE_RESPONSE:
            decoded = self.decode_response(msg_parts)
        elif msg_type == MessageType.TYPE_INFO:
            decoded = self.decode_log(msg_parts)
        else:
            raise Exception('Message type not supported')
        return decoded

    def decode_request(self, msg_parts):

        # get class name/path
        classname = msg_parts[1].split('=')[1]
        classpath = msg_parts[2].split('=')[1]

        # get parameters
        parameters = dict()
        for t in msg_parts[3:]:
            k, v = t.split('=')
            parameters[k] = v

        # build request
        request = Request()
        request.set_classname(classname)
        request.set_classpath(classpath)
        request.set_data(parameters)

        return request

    def decode_response(self, msg_parts):

        # get status
        status = msg_parts[1].split('=')[1]

        # get description
        if len(msg_parts) == 3:
            description = msg_parts[2].split('=')[1]
        else:
            description = None

        # build response
        response = Response()
        response.set_status(status)
        if description:
            response.set_description(description)

        return response


if __name__ == '__main__':

    info = Info()
    info.content = 8
    print(info.content)
