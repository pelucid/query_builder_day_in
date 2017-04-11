"""API base classes and functions

- auth_required: used as a decorator for all the authenticated calls
- APIHandler: the base class for all handlers
- ErrorHandler: custom error handler
"""

import datetime
import ujson

import tornado.web
import tornado.httpclient

from query_builder import exceptions


class APIHandler(tornado.web.RequestHandler):
    """Base class for all API handlers"""

    SUPPORTED_METHODS = ("GET")

    def __init__(self, *args, **kwargs):
        super(APIHandler, self).__init__(*args, **kwargs)
        self.app = self.application
        self.piston = self.app.piston
        self.parsed_params = {}

    @property
    def log(self):
        """Get a logger object
        This object is configured with the user ID if possible."""

        log = self.application.log
        return log

    def write_error(self, status_code, **kwargs):
        """Overwritten method to send a proper JSON response in case of error

        This function executes when Tornado gets an unhandled exception. This
        results in a 500 (our fault)."""

        # NOTE (for reference): print kwargs["exc_info"]
        if status_code == 500:
            self.send(err="Error " + str(status_code), code=500)
        else:
            self.send(err="Error " + str(status_code), code=status_code)

    def send(self, content=None, err="", info="", code=None, format_="json",
             top_level_dict=None, filename=None, redirect_location=None):
        """Send return data, content is JSON encoded.

        Arguments:
            content: Python structure to be returned as JSON by the API
            err: error message to be sent in the top-level "err" field
            info: info message to be sent in the top-level "info" field
            code: HTTP status code returned by the server, default is 200
            format: json or csv
            top_level_dict: dictionary of fields to be inserted at the top

        Returns:
            None
        """
        output = {"version": self.app.version}

        if top_level_dict:
            output.update(top_level_dict)

        # Format error message and set the error code
        output["err"] = err
        if err and not code:
            code = 400

        if code:
            self.set_status(code)

        # Set the data and add a count if data is a list
        output["data"] = content
        if isinstance(content, list):
            output["count"] = len(content)

        # Set the info message
        duration = 1000.0 * self.request.request_time()
        if not info:
            output["info"] = "Call time: {0}ms".format(round(duration, 2))
        else:
            output["info"] = str(info)

        # Set the headers and go!
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Headers",
                        "content-type,accept,origin,X-HTTP-Method-Override")
        self.set_header("Cache-Control", "no-cache")

        if redirect_location:
            self.set_header("Location", redirect_location)

        if format_ == "json":
            self.write(ujson.dumps(output))
        elif format_ == "salesforce":
            self.send_to_peaches(content, filename)
        elif format_ == "csv":
            date = datetime.datetime.now().strftime("%Y%m%d_%H%M")
            self.set_header("Content-Type", "text/plain")

            if not filename:
                filename = "gi_export_{}.csv".format(date)
            elif filename[-4:] != ".csv":
                filename = "{}.csv".format(filename)

            self.set_header("Content-Disposition",
                            'attachment; filename="{}"'.format(filename))

            self.write(content)

    def validate_args(self, valid_arguments=None, required_args=None):
        """Check argument parameters are valid and present raise exception if not"""
        request_set = set(self.request.arguments)
        if valid_arguments:
            invalid = request_set - set(valid_arguments)
            if invalid:
                raise exceptions.ParameterKeyError(key=", ".join(invalid))

        if required_args:
            missing = set(required_args) - request_set
            if missing:
                raise exceptions.ParameterKeyError(key=", ".join(missing))

    def _safe_deserialize(self, serializer, data, partial=False):
        deserialized = serializer().load(data, partial=partial)
        if deserialized.errors:
            raise exceptions.ClientError(self._format_serializer_errors(deserialized.errors))
        return deserialized.data

    def _format_serializer_errors(self, errors):
        error_str = ""
        for k, v in errors.items():
            error_str += "{}: {};".format(k, " ".join(v))
        return error_str




class ErrorHandler(APIHandler):
    """Handle 404 errors, all other ones are handled at the APIHandler level"""

    def __init__(self, application, request, status_code):
        APIHandler.__init__(self, application, request)
        self.set_status(status_code)

    def write_error(self, status_code, **kwargs):
        self.send(err="Error " + str(self._status_code),
                  code=self._status_code)

    def prepare(self):
        raise tornado.web.HTTPError(self._status_code)


def exception_handling(method):
    """Decorate get() to catch our custom exceptions

    NOTE: Be sure to have this decorator be the innermost one so we get to the
    exception before Tornado does."""

    # HTTP Codes:
    # 400 Bad Request
    # 503 Service Unavailable

    # TODO: decide whether to deal with unhandled exceptions here or with
    # Tornado's hook (ErrorHandler)

    def tryexcept_wrapper(self, *args, **kwargs):
        try:
            method(self, *args, **kwargs)

        except exceptions.NonExistingObjectError as e:
            self.send(err=e.msg, code=404)

        except exceptions.ActionNotAllowed as e:
            self.send(err=e.msg, code=403)

        except exceptions.ConflictingDataError as e:
            self.send(err=e.msg, code=409)

        except exceptions.ClientError as e:
            self.send(err=e.msg, code=400)

        except exceptions.MalformedModelConfigException as e:
            self.send(err=e.msg, code=500)

        except exceptions.ServiceError as e:
            if (self.auth_user and hasattr(self.auth_user, "email") and
                    self.auth_user.email):
                _msg = "Username: {0}, details: {1}"
                err_log = _msg.format(self.auth_user.email, e.details)
            else:
                _msg = "Username: (debug), details: {0}"
                err_log = _msg.format(e.details)
            self.app.error_log.critical(err_log)
            self.send(err=e.msg, code=503)

        except (exceptions.EsBadRequest, exceptions.ESQueryError) as e:
            self.send(err=e.msg, code=400)
            if hasattr(self.user, "username") and hasattr(self.user, "email"):
                _msg = "Username: {0}, email: {1}, details: {2}"
                err_log = _msg.format(self.user.username, self.user.email,
                                      e.details)
            else:
                _msg = "Unknown user, details: {0}"
                err_log = _msg.format(e.details)

            self.app.error_log.error(err_log)

    return tryexcept_wrapper
