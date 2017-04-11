import pytest

from query_builder.tests.end_to_end.es_query_template import full_es_query
from query_builder.tests.pytest_utils import fetch_json, build_complete_url


@pytest.mark.gen_test
def test_one_value(http_client, base_url):
    url = build_complete_url(base_url,
                             "/v1/company_query_builder?cid=1")
    response = yield fetch_json(http_client, url)
    assert response == full_es_query({
        'terms': {
            'cid': [
                '1'
            ]
        }
    })

@pytest.mark.gen_test
def test_multiple_values(http_client, base_url):
    url = build_complete_url(base_url,
                             "/v1/company_query_builder?cid=1&cid=2&cid=100")
    response = yield fetch_json(http_client, url)
    assert response == full_es_query({
        'terms': {
            'cid': ['1', '2', '100']
        }
    })