import pytest

from query_builder.tests.end_to_end.es_query_template import full_es_query
from query_builder.tests.pytest_utils import fetch_json, build_complete_url


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


@pytest.mark.gen_test
def test_range_both_ends(http_client, base_url):
    url = build_complete_url(base_url,
                             "/v1/company_query_builder?revenue=1-100")
    response = yield fetch_json(http_client, url)
    assert response == revenue_range_template(1, 100)

@pytest.mark.gen_test
def test_range_bottom_end(http_client, base_url):
    url = build_complete_url(base_url,
                             "/v1/company_query_builder?revenue=1-")
    response = yield fetch_json(http_client, url)
    assert response == revenue_range_template(1, None)

@pytest.mark.gen_test
def test_range_top_end(http_client, base_url):
    url = build_complete_url(base_url,
                             "/v1/company_query_builder?revenue=-100")
    response = yield fetch_json(http_client, url)
    assert response == revenue_range_template(None, 100)
