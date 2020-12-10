from src.flask_test import config
from src.flask_test.core import create_app

app = create_app(config.DevelopmentConfig)


@app.shell_context_processor
def make_shell_context():
    from src.flask_test.db import db

    return {
        "db": db
    }
