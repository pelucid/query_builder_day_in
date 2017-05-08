"""

Usage:
    main.py <url_path>

Options:
    <url_path> - URL path with query parameters to turn into query.
                 e.g. /v1/company_query_builder?revenue=20150101-20160101
                 
"""
import json

import docopt

from query_builder.app import handlers


def get_es_query(request_url):
    """
    Given a request URL path with query parameters, return an elasticsearch query
    Args:
        request_url: path with query parameters, string

    Returns:
        Dictionary - elasticsearch query
    """
    handler = handlers.CompanyQueryBuilder(request_url)
    return handler.get()


if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    es_query = get_es_query(args['<url_path>'])
    print json.dumps(es_query, indent=2)
