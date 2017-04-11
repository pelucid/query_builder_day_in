"""
Helper functions for building elasticsearch queries and filters.
"""


def dates_for_date_range(params, dates_key):
    """Construct dates for a date range filter or query

    Args:
        params: query parameters dict
        dates_key: the 'type' of dates to be looked for
    """
    gte = None
    lte = None

    if dates_key in params:
        gte = params[dates_key].get("gte", None)
        lte = params[dates_key].get("lte", None)

    return gte, lte


def build_child_doc_filter(doc_type, date_name, gte, lte):
    """Construct a child document filter

    Args:
        doc_type: the type of child doc to search for
        date_name: the name of the date to filter by
        gte: the 'from' date
        lte: the 'to' date
    """

    child_doc_filter = {
        "has_child": {
            "type": doc_type,
            "filter": {
                "and": [
                    {
                        "range": {
                            date_name: {
                                "gte": gte,
                                "lte": lte
                            }
                        }
                    }
                ]
            }
        }
    }

    return child_doc_filter


def range_(variable, gte, lte):
    """Create a range query for Elasticsearch."""

    query = {
        'range': {
            variable: {}
        }
    }

    if gte:
        query['range'][variable]['gte'] = gte

    if lte:
        query['range'][variable]['lte'] = lte

    return query


def financial_filters_range(financial_field, range_dict):
    """Create a range query for Elasticsearch using latest financials where
       range_dict contains:
        {
            "gte": <lower_bound>,
            "lte": <upper_bound>,
        }
    """
    ranges = {}
    lower_bound = range_dict.get('gte')
    upper_bound = range_dict.get('lte')
    # if lower bound is zero don't add it - we want to include negative values
    if lower_bound:
        ranges['gte'] = lower_bound
    if upper_bound is not None:
        ranges['lte'] = range_dict.get('lte')

    range_field = "financial_filters.{}".format(financial_field)
    query = {
        "nested": {
            "path": "financial_filters",
            "filter": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                range_field: ranges
                            }
                        }
                    ]
                }
            }
        }
    }
    return query


def _exists_filter(field):
    """Create an exists filter for Elasticsearch"""

    return {
        "exists": {
            "field": field
        }
    }


def exact_matches(variable, values, minimum_match=None):
    """Create a terms query for Elasicsearch."""

    dsl = {
        "terms": {
            variable: values
        }
    }

    # Only applicable to queries, not filters
    if minimum_match:
        dsl['terms']['minimum_match'] = minimum_match

    return dsl


def _and_filter(filter_list):
    """Create a AND filter for Elasticsearch.

    Takes a list of filters and creates an AND filter DSL. Returns an empty
    dict if there are no filters.
    """

    filter_dsl = {}
    if filter_list:
        filter_dsl['and'] = filter_list

    return filter_dsl


def _field_function(field):
    """Return a function score query component based on the field name"""

    return {
        "field_value_factor": {
            "field": field
        }
    }


def _bool_query():
    """Return a template for a bool query"""

    return {
        "bool": {
            "must": {
                "match_all": {}
            },
            "should": []
        }
    }
