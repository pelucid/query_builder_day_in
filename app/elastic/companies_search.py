"""This module contains helpers for building up search queries."""

import query_builder.app.elastic.filters as es_filter



def _get_generic_filters(params):
    """Compile all the filters in the query."""
    filters = [
        {
            "term": {
                "status": 1
            }
        }
    ]

    filters += es_filter.basic_filters(params)
    filters += es_filter.trading_activity_filters(params)
    filters += es_filter.cids_filters(params)

    filter_dsl = {}
    if filters:
        filter_dsl = {'and': filters}

    return filter_dsl


def vanilla_query():
    """Return a vanilla query"""

    query = {
        "query": {
            "filtered": {
                "filter": {
                    "and": []
                }
            }
        }
    }
    return query

def _add_fields_pagination(es_query, params):
    """Function adds fields and pagination params to query.

    Fields are the requested fields to be returned.
    Pagination parameters is the number of results and offset to return.
    """

    if "size" in params:
        es_query["size"] = params["size"]

    if "from" in params:
        es_query["from"] = params["from"]

    if "fields" in params:
        es_query["fields"] = params["fields"]

    return es_query


def query_builder(params):
    """Build the companies search query.

    This method also returns instructions on how to colour the results
    """
    query_dsl = vanilla_query()

    filter_dsl = _get_generic_filters(params)

    # Add the filters to the query:
    query_dsl["query"]["filtered"]["filter"]["and"] += filter_dsl["and"]

    # Pagination
    query_dsl = _add_fields_pagination(query_dsl, params)

    return query_dsl