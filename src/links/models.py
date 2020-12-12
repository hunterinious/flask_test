from src.flask_test.db import db
from datetime import datetime, timedelta


class Link(db.Model):
    __tablename__ = 'links'
    id = db.Column(db.Integer, primary_key=True)
    short_url = db.Column(db.String(8), unique=True, nullable=False)
    long_url = db.Column(db.String(2048), nullable=False)
    expire_date = db.Column(db.TIMESTAMP(timezone=False), nullable=False, default=datetime.now() + timedelta(days=90))
