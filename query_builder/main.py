import json

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
    es_query = get_es_query("/v1/company_query_builder?revenue=20150101-20160101")
    print json.dumps(es_query, indent=4)
