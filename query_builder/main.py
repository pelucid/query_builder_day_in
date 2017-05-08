import json

from query_builder.app import handlers

if __name__ == "__main__":
    request_url = "/v1/company_query_builder?revenue=20150101-20160101"
    handler = handlers.CompanyQueryBuilder(request_url)
    es_query = handler.get()
    print json.dumps(es_query, indent=4)
