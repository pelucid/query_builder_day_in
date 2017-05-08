"""ES querying layer."""


import datetime
import json
import logging
import os


from query_builder.config import settings
from query_builder import __file__ as api_path
from query_builder.app.elastic import companies_search

api_version = settings.app_settings["version"]



class Piston(object):
    """Logic for converting parameter dictionaries into Elasticsearch Query"""

    def __init__(self, logger=None):

        api_directory = os.path.dirname(os.path.abspath(api_path))
        if logger:
            self.log = logger
        else:
            self.log = logging.getLogger("query_builder.piston")
            self.log.setLevel(logging.DEBUG)
            log_path = "{0}/logs/query_builder.piston.log".format(api_directory)
            f_handler = logging.FileHandler(log_path)
            self.log.addHandler(f_handler)

        log_format = ("%(asctime)s - "
                      "v{0} - %(levelname)s - %(message)s".format(api_version))
        self.queries_log = logging.getLogger("query_builder.piston.queries")
        self.queries_log.setLevel(logging.DEBUG)
        self.queries_log.propagate = False
        log_path = "{0}/logs/query_builder.piston.queries.log".format(api_directory)
        f_handler = logging.FileHandler(log_path)
        formatter = logging.Formatter(log_format)
        f_handler.setFormatter(formatter)
        self.queries_log.addHandler(f_handler)
        self.dthandler = (lambda obj: obj.isoformat()
                            if isinstance(obj, datetime.datetime) or
                               isinstance(obj, datetime.date)
                            else None)


    def _log_query(self, query):
        """Write ES query to log file.

        Args:
            query: ES query as a python dict
        """
        self.queries_log.debug("doc_type: {0}, query: {1}".format("company",
                            json.dumps(query, default=self.dthandler)))


    def company_search(self, params):
        """Search for companies by any parameter.

        Arguments:
            params: dictionary of params.
        Returns:
            list of _source documents returned by ES.
        """
        # Build the query from the params
        es_query = companies_search.query_builder(params)
        self._log_query(es_query)


        return es_query
