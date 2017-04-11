import pytest
from tornado.httpclient import HTTPError

from query_builder.tests.pytest_utils import fetch_json, build_complete_url


@pytest.mark.parametrize('url', [
    '/v1/company_query_builder?cid=1',
    '/v1/company_query_builder?sector_context=3',
    '/v1/company_query_builder?ecommerce=true',
    '/v1/company_query_builder?cash=0-1000',
    '/v1/company_query_builder?revenue=0-1000',
    '/v1/company_query_builder?aggregate=true',
    '/v1/company_query_builder?exclude_tps=true',
    '/v1/company_query_builder?trading_activity=20150101-20160101',
])
@pytest.mark.gen_test
def test_all(http_client, base_url, url):
    _url = build_complete_url(base_url, url)
    try:
        response = yield fetch_json(http_client, _url)
    except HTTPError:
        raise Exception("Call to {} failed".format(url))