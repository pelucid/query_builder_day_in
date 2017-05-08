from query_builder.main import get_es_query
from query_builder.tests.end_to_end.es_query_template import full_es_query


def test_boolean_true():
    url = "/v1/company_query_builder?ecommerce=true"
    response = get_es_query(url)
    assert response == full_es_query({
        'term': {
            'ecommerce.is_ecommerce': True
        }
    })

def test_boolean_false():
    url = "/v1/company_query_builder?ecommerce=false"
    response = get_es_query(url)
    assert response == full_es_query(None)