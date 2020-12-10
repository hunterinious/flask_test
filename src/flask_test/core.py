import flask


def create_app(config):
    app = flask.Flask(__name__)
    app.config.from_object(config)

    from src.flask_test.db import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    from flask_restful import Api
    api = Api(app, prefix="/api")
    add_resources(api)

    from flask_cors import CORS
    CORS(app)

    return app


def add_resources(api):
    pass
