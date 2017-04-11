import pytest

from query_builder.tests.end_to_end.es_query_template import full_es_query
from query_builder.tests.pytest_utils import fetch_json, build_complete_url


@pytest.mark.gen_test
def test_boolean_true(http_client, base_url):
    url = build_complete_url(base_url,
                             "/v1/company_query_builder?ecommerce=true")
    response = yield fetch_json(http_client, url)
    assert response == full_es_query({
        'term': {
            'ecommerce.is_ecommerce': True
        }
    })

@pytest.mark.gen_test
def test_boolean_false(http_client, base_url):
    url = build_complete_url(base_url,
                             "/v1/company_query_builder?ecommerce=false")
    response = yield fetch_json(http_client, url)
    assert response == full_es_query(None)