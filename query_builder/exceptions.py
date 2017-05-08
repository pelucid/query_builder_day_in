"""Module for defining API Exceptions."""


class ClientError(Exception):
    def __init__(self, msg):
        super(ClientError, self).__init__(msg)
        self.message = self.msg = msg


class ESQueryError(Exception):
    """Exception related to building the ES query structure."""

    def __init__(self, err, method):
        self.msg = "Query build error"
        self.details = "{}: {}".format(method, err)


class ParameterKeyError(ClientError):
    def __init__(self, key):
        super(ParameterKeyError, self).__init__("Key Error: {}".format(key))


class ParameterValueError(ClientError):
    def __init__(self, key, value, message=''):
        if message:
            message = ' - ' + message
        super(ParameterValueError, self).__init__(
            u"Value Error for key '{}': {}{}".format(key, value, message))
