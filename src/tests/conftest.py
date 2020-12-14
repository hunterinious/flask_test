import pytest
from src.flask_test.core import create_app


@pytest.fixture(scope='session')
def app():
    testapp = create_app('src.flask_test.config.TestConfig')
    return testapp
