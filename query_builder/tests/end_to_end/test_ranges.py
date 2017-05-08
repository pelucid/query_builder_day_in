from query_builder.main import get_es_query
from query_builder.tests.end_to_end.es_query_template import full_es_query


def revenue_range_template(gte=None, lte=None):
    gte_lte = dict()
    if gte:
        gte_lte['gte'] = gte
    if lte:
        gte_lte['lte'] = lte

    return full_es_query({
        "nested": {
            "filter": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "financial_filters.revenue": gte_lte
                            }
                        }
                    ]
                }
            },
            "path": "financial_filters"
        }
    })


def test_range_both_ends():
    url = "/v1/company_query_builder?revenue=1-100"
    response = get_es_query(url)
    assert response == revenue_range_template(1, 100)

def test_range_bottom_end():
    url = "/v1/company_query_builder?revenue=1-"
    response = get_es_query(url)
    assert response == revenue_range_template(1, None)

def test_range_top_end():
    url = "/v1/company_query_builder?revenue=-100"
    response = get_es_query(url)
    assert response == revenue_range_template(None, 100)
