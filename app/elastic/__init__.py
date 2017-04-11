#!/usr/bin/env python

from query_builder.exceptions import ESQueryError

def query_build_exception(method):
    """Decorate query building methods.

    Catch exceptions related to malformed ES Queries.
    """

    def wrapper(self, *args, **kwargs):

        try:
            return method(self, *args, **kwargs)
        except AttributeError as e:
            raise ESQueryError(e, method.__name__)

    return wrapper
