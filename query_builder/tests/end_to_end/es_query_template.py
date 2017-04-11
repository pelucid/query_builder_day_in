def full_es_query(sub_query):
    full = {
        "query": {
            "filtered": {
                "filter": {
                    "and": [
                        {
                            "term": {
                                "status": 1
                            }
                        }
                    ]
                }
            }
        },
        "from": 0,
        "size": 50
    }
    if sub_query:
        full['query']['filtered']['filter']['and'].append(sub_query)
    return full
