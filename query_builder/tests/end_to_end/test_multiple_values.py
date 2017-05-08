import pytest

from query_builder.main import get_es_query
from query_builder.tests.end_to_end.es_query_template import full_es_query


def test_one_value():
    url = "/v1/company_query_builder?cid=1"
    response = get_es_query(url)
    assert response == full_es_query({
        'terms': {
            'cid': [
                '1'
            ]
        }
    })

@pytest.mark.gen_test
def test_multiple_values():
    url = "/v1/company_query_builder?cid=1&cid=2&cid=100"
    response = get_es_query(url)
    assert response == full_es_query({
        'terms': {
            'cid': ['1', '2', '100']
        }
    })