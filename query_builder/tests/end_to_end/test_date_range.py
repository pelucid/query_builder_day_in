from query_builder.main import get_es_query
from query_builder.tests.end_to_end.es_query_template import full_es_query

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


def test_date_range_both_ends():
    url = "/v1/company_query_builder?trading_activity=20150101-20160101"
    response = get_es_query(url)
    assert response == trade_activity_template("2015-01-01", "2016-01-01")

def test_date_range_bottom_end():
    url = "/v1/company_query_builder?trading_activity=20150101-"
    response = get_es_query(url)
    assert response == trade_activity_template("2015-01-01", None)

def test_date_range_upper_end():
    url = "/v1/company_query_builder?trading_activity=-20160101"
    response = get_es_query(url)
    assert response == trade_activity_template(None, "2016-01-01")
