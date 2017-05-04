#!/usr/bin/env python
"""Growth Intelligence query_builder."""

import os
import os.path
import datetime
import argparse
import logging
import re
import json
import glob
import sys

import tornado
import tornado.web
import tornado.options

from query_builder.app.handlers.base import ErrorHandler
from query_builder.config import routes
import query_builder.app.elastic.piston as piston


from query_builder.config import settings

api_version = settings.app_settings["version"]


# Directory of current file (main.py)
api_directory = os.path.dirname(os.path.abspath(__file__))

# Create logs directory if it doesn't exist
log_directory = os.path.join(api_directory, "logs")
if not os.path.exists(log_directory):
    os.mkdir(log_directory)

log_format = ("%(asctime)s - %(name)s - L%(lineno)d - "
              "v{0} - %(levelname)s - %(message)s".format(api_version))


def setup_logger(logger_name, path, level, propagate=False):
    logger = logging.getLogger(logger_name)
    logger.setLevel(getattr(logging, level.upper()))
    logger.propagate = propagate
    f_handler = logging.FileHandler(path)
    formatter = logging.Formatter(log_format)
    f_handler.setFormatter(formatter)
    logger.addHandler(f_handler)


def setup_loggers():
    """Setup loggers and handlers for third party libraries."""

    setup_logger("", "logs/root.log", "debug")
    setup_logger("elasticsearch", "logs/elasticsearch.log", "info")

    # TODO: Test whether DEBUG is reasonable. It writes the results from ES in
    # indented (pretty) JSON format. INFO only writes the queries.
    setup_logger("elasticsearch.trace", "logs/elasticsearch.trace.log", "info")

    setup_logger("urllib3", "logs/urllib3.log", "info")
    setup_logger("tornado", "logs/tornado.log", "debug")
    setup_logger("tornado.access", "logs/tornado.access.log", "debug", True)
    setup_logger(
        "tornado.application", "logs/tornado.application.log", "debug", True)
    setup_logger("tornado.general", "logs/tornado.general.log", "debug", True)
    setup_logger("tldextract", "logs/tldextract.log", "debug", True)
    logging.getLogger('boto').setLevel(logging.INFO)


# Used by the unit tests to close loggers after a test is completed
def shutdown_loggers():
    """Close all the logging file handles."""

    lgs = ["tornado.general", "tornado.application", "tornado.access",
           "tornado", "urllib3", "elasticsearch", ""]

    for lger in lgs:
        logger = logging.getLogger(lger)
        for h in logger.handlers:
            h.close()


class Application(tornado.web.Application):
    def __init__(self, port=10000, settings=None, autoreload=False):
        """Main API Application.

        Arguments
            port: int
            settings
            autoreload (bool): Reload API in dev mode
        """

        if not settings:
            from query_builder.config import settings

        self.settings = settings.app_settings
        self.version = self.settings["version"]

        # Setup loggers for third party libraries
        setup_loggers()

        formatter = logging.Formatter(log_format)

        # API access logger
        self.access_log = logging.getLogger('query_builder.main.access')
        self.access_log.propagate = False
        self.access_log.setLevel(logging.INFO)
        for log_path_dir in ['{0}/logs/'.format(api_directory)]:
            log_path = log_path_dir + 'query_builder.main.access-{0}.log'.format(port)
            f_handler = logging.FileHandler(log_path)
            f_handler.setFormatter(formatter)
            self.access_log.addHandler(f_handler)

        # API handled errors
        self.error_log = logging.getLogger('query_builder.main.error')
        self.error_log.propagate = False
        self.error_log.setLevel(logging.WARNING)
        for log_path_dir in ['{0}/logs/'.format(api_directory)]:
            log_path = log_path_dir + 'query_builder.main.error.log'
            f_handler = logging.FileHandler(log_path)
            f_handler.setFormatter(formatter)
            self.error_log.addHandler(f_handler)

        # App log for debugging and non-important messages (restarting the
        # server, for example)
        self.log = logging.getLogger('query_builder.main.info')
        self.log.propagate = False
        self.log.setLevel(logging.INFO)
        for log_path_dir in ['{0}/logs/'.format(api_directory)]:
            log_path = log_path_dir + 'query_builder.main.info.log'
            f_handler = logging.FileHandler(log_path)
            f_handler.setFormatter(formatter)
            self.log.addHandler(f_handler)

        self.port = port

        self.piston_log = logging.getLogger('query_builder.piston')
        self.piston_log.propagate = False
        self.piston_log.setLevel(logging.INFO)
        log_path = '{0}/logs/query_builder.piston.log'.format(api_directory)
        f_handler = logging.FileHandler(log_path)

        f_handler.setFormatter(formatter)
        self.piston_log.addHandler(f_handler)

        self.piston = piston.Piston(self.piston_log)

        super(Application, self).__init__(routes.ROUTES, autoreload=autoreload, **self.settings)

    def log_request(self, handler):
        """Overridden method to log completed HTTP requests.

        "Completed requests" mean Tornado returned an HTTP response but
        not necessarily valid JSON or even a body."""

        if handler.get_status() < 400:
            log_method = self.access_log.info
        elif handler.get_status() < 500:
            log_method = self.access_log.warn
        else:
            log_method = self.access_log.error

        request_time = 1000.0 * handler.request.request_time()
        try:
            key = str(handler.key)
        except AttributeError:
            key = ""
        try:
            username = handler.auth_user.email
        except AttributeError:
            username = "(no user)"
        try:
            org = "{}".format(str(handler.auth_user.org_id)) or "no org"
        except AttributeError:
            org = "unknown org"

        if (hasattr(handler, "request") and
                hasattr(handler.request, "headers") and
                    "X-Real-Ip" in handler.request.headers and
                handler.request.headers["X-Real-Ip"]):
            real_ip_re = re.search("[0-9]{1,3}\.[0-9]{1,3}\."
                                   "[0-9]{1,3}\.[0-9]{1,3}",
                                   handler.request.headers["X-Real-Ip"])
            if real_ip_re:
                real_ip = real_ip_re.group()
            else:
                real_ip = handler.request.headers["X-Real-Ip"]
        else:
            real_ip = "unknown IP"

        log_message = "status_code: %d - real_ip: %s - %.2fms %s (%s) - %s" % (
            handler.get_status(), real_ip, request_time, username, org,
            handler._request_summary())
        log_method(log_message)


def serve(port, autoreload):
    """Start the API server."""

    # Custom 400s errors handling
    tornado.web.ErrorHandler = ErrorHandler

    # Turn on traceback on stdout for development debugging
    try:
        # Tornado 2
        tornado.options.enable_pretty_logging()
    except AttributeError:
        # Tornado 3
        tornado.log.enable_pretty_logging()

    # Instantiate the app and launch the IOLoop
    application = Application(port=port, autoreload=autoreload)
    application.listen(port)
    application.log.info("Starting API server on port " + str(port))
    print "\n{}: API online on port {}".format(datetime.datetime.now(), port)

    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8010,
                        help='port number the server will run on')
    parser.add_argument('--autoreload', type=bool, default=False,
                        help='reload server when files change')
    args = parser.parse_args()
    serve(args.port, args.autoreload)
