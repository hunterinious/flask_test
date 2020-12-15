import os


class DevelopmentConfig(object):
    DEBUG = True

    JSON_AS_ASCII = False

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DB_URI',
        'postgresql://test:test@127.0.0.1:5432/test_task'
        )
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestConfig(object):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST_DB_URI',
        'postgresql://test:test@127.0.0.1:5432/test'
        )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
