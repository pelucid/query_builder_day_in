"""Module for defining API Exceptions."""


class ClientError(Exception):
    def __init__(self, msg):
        super(ClientError, self).__init__(msg)
        self.msg = msg


class ESQueryError(Exception):
    """Exception related to building the ES query structure."""

    def __init__(self, err, method):
        self.msg = "Query build error"
        self.details = "{}: {}".format(method, err)


class UrlError(ClientError):
    def __init__(self, url):
        self.msg = "Bad URL: {}".format(url)


class ParameterKeyError(ClientError):
    def __init__(self, key):
        self.msg = "Key Error: {}".format(key)


class ParameterValueError(ClientError):
    def __init__(self, key, value, message=''):
        if message:
            message = ' - ' + message
        self.msg = u"Value Error for key '{}': {}{}".format(key, value, message)


class ModelNotFound(ClientError):
    def __init__(self, model, org):
        self.msg = u"Model {} not found in available models for {}".format(model, org)


class ModelNotSet(ClientError):
    def __init__(self):
        self.msg = u"Cannot perform operation as a model has not been specified"


class MalformedModelConfigException(Exception):
    def __init__(self, model_version, score_version, thresholds):
        self.msg = u"Model config malformed: (model_version: {}, score_version: {}, thresholds: {})".format(
                        model_version, score_version, ", ".join(str(i) for i in thresholds))


class ActionNotAllowed(ClientError):
    def __init__(self, action_description, user, org):
        self.msg = u"Action not allowed for user {} from org {}. {}".format(
            user, org, action_description)


class NonExistingObjectError(ClientError):
    def __init__(self, obj):
        self.msg = "No resource for: {}".format(obj)


class UnexpectedDataError(ClientError):
    def __init__(self, data):
        self.msg = "Unexpected data in request body: {}".format(data)


class ConflictingDataError(ClientError):
    def __init__(self, msg):
        self.msg = msg


class UnexpectedEncodingError(Exception):
    def __init__(self, data):
        self.msg = u"Unexpected bytes: {}".format(data)


class ServiceError(Exception):
    """Exception to be used when ES, Redis or other services are down.

    Argument:
        details: additional information from Redis / ES."""

    def __init__(self, details=""):
        self.msg = "Service unavailable"
        self.details = details


class EsBadRequest(Exception):
    """Exception to be used when ES doesn't know how to process the request.

    Argument:
        details: additional information from Redis / ES."""

    def __init__(self, details=""):
        self.msg = "Unexpected data"
        self.details = details
