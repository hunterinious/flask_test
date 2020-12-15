import flask


def create_app(config):
    app = flask.Flask(__name__)
    app.config.from_object(config)

    from src.flask_test.db import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    from src.flask_test.marshmallow import ma
    ma.init_app(app)

    from src.flask_test.crontab import crontab
    crontab.init_app(app)
    add_crontabs(crontab)

    from flask_restful import Api
    api = Api(app, prefix="/api")
    add_resources(api)

    from flask_cors import CORS
    CORS(app)

    return app


def add_resources(api):
    from src.links.resources import CreateLinkAPI, RetrieveLinkAPI, LinkRedirectAPI

    api.add_resource(CreateLinkAPI, '/links/create')
    api.add_resource(RetrieveLinkAPI, '/links/<int:id>/retrieve')
    api.add_resource(LinkRedirectAPI, '/links/<int:id>/redirect')


def add_crontabs(crontab):
    from src.links.models import Link

    @crontab.job(minute="1")
    def set_is_expired_for_all_links():
        Link.set_is_expired_for_all_links()

