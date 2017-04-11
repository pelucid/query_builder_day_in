import pytest

from query_builder.tests.end_to_end.es_query_template import full_es_query
from query_builder.tests.pytest_utils import fetch_json, build_complete_url

def trade_activity_template(gte=None, lte=None):
    gte_lte = {'gte': gte, 'lte': lte}

    return full_es_query(
        {
            "or": [
                {
                    "has_child": {
                        "filter": {
                            "and": [
                                {
                                    "range": {
                                        "import_date": gte_lte
                                    }
                                }
                            ]
                        },
                        "type":"import_events"
                    }
                },
                {
                    "has_child": {
                        "filter": {
                            "and": [
                                {
                                    "range": {
                                        "date": gte_lte
                                    }
                                }
                            ]
                        },
                        "type":"export_events"
                    }
                }
            ]
        }
    )


@pytest.mark.gen_test
def test_date_range_both_ends(http_client, base_url):
    url = build_complete_url(base_url,
                             "/v1/company_query_builder?trading_activity=20150101-20160101")
    response = yield fetch_json(http_client, url)
    assert response == trade_activity_template(1420070400, 1451606400)

@pytest.mark.gen_test
def test_date_range_bottom_end(http_client, base_url):
    url = build_complete_url(base_url,
                             "/v1/company_query_builder?trading_activity=20150101-")
    response = yield fetch_json(http_client, url)
    assert response == trade_activity_template(1420070400, None)

@pytest.mark.gen_test
def test_date_range_upper_end(http_client, base_url):
    url = build_complete_url(base_url,
                             "/v1/company_query_builder?trading_activity=-20160101")
    response = yield fetch_json(http_client, url)
    assert response == trade_activity_template(None, 1451606400)
