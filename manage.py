from src.flask_test import config
from src.flask_test.core import create_app
import os


conf = os.environ.get('ENV', 'development')
if conf == 'development':
    app = create_app(config.DevelopmentConfig)
elif conf == 'test':
    app = create_app(config.TestConfig)


@app.shell_context_processor
def make_shell_context():
    from src.flask_test.db import db

    return {
        "db": db
    }
