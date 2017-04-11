import json
from tornado import gen


@gen.coroutine
def fetch_json(client, url):
    """Wondering what is happening here?
    http://tornado.readthedocs.io/en/latest/gen.html#tornado.gen.Return
    """
    response = yield fetch(client, url)
    raise gen.Return(json.loads(response.body)["data"])


def fetch(client, url, **kwargs):
    return client.fetch(url, **kwargs)


def build_complete_url(base, url):
    return "{}{}".format(base, url)