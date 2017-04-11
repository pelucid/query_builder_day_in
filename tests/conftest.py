import pytest

from query_builder import main
from query_builder.config import settings


@pytest.fixture
def app(http_port):
    """Used by pytest-tornado clients.
    We patch the app so that all it's handlers rely on the same session and the
    factories that generate our fixture.
    """
    app = main.Application(settings=settings, port=http_port)
    return app