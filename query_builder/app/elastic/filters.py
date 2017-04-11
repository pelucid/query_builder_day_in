#!/usr/bin/env python
"""Contains functions for building filters in ES queries."""

from query_builder.app.elastic import (query_helpers, query_build_exception)
from query_builder.config import settings


def basic_filters(params):
    """Build up basic filters.

    p - parameters passed to query builder.
    """
    filters = []
    if "revenue" in params:
        filt = query_helpers.financial_filters_range("revenue", params["revenue"])
        filters.append(filt)

    if "cash" in params:
        f = query_helpers.financial_filters_range("cash", params["cash"])
        filters.append(f)

    if "sectors" in params:
        filters.append(query_helpers.exact_matches(settings.SECTOR_ES_FIELD,
                                                   params["sectors"]))

    if 'ecommerce' in params:
        filters.append({"term": {"ecommerce.is_ecommerce": True}})

    if 'exclude_tps' in params:
        f = {"missing": {"field": "tps"}}
        filters.append(f)

    return filters


@query_build_exception
def trading_activity_filters(params):
    """Add trading activity filters to query"""

    filters = []
    if "trading_activity" in params:
        gte, lte = query_helpers.dates_for_date_range(params,
                                                      'trading_activity')
        imports_filter = query_helpers.build_child_doc_filter(
            'import_events', 'import_date', gte, lte)
        exports_filter = query_helpers.build_child_doc_filter(
            'export_events', 'date', gte, lte)
        filters.append(imports_filter)
        filters.append(exports_filter)
        filters = [{"or": filters}]
    return filters

def cids_filters(params):
    """Add CIDS to filters."""

    if "cids" not in params:
        return []

    cids_filter = {
        "terms": {
            "cid": params["cids"]
        }
    }

    return [cids_filter]
