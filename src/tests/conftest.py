from src.flask_test.core import create_app
from src.flask_test.db import db
from src.links.populate_db import create_links_from_json
import os.path as op
import pytest
import json


CURRENT_PATH = op.dirname(__file__)


@pytest.fixture(scope='session')
def app():
    testapp = create_app('src.flask_test.config.TestConfig')
    return testapp


@pytest.fixture(scope='function')
def db_fixture():
    db.engine.execute('DROP SCHEMA IF EXISTS public CASCADE')
    db.engine.execute('CREATE SCHEMA public')
    db.configure_mappers()
    db.create_all()

    return db


@pytest.fixture
def fill_links_fixture():
    links_path = op.join(CURRENT_PATH, 'sources', 'links.json')
    with open(links_path) as f:
        return create_links_from_json(json.load(f))
