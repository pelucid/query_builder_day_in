import pytest

from query_builder.main import get_es_query


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
def test_all(url):
    get_es_query(url)
