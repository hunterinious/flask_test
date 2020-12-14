from src.flask_test.db import db
from datetime import datetime, timedelta
from base64 import b32encode
import os


class Link(db.Model):
    __tablename__ = 'links'
    id = db.Column(db.Integer, primary_key=True)
    short_url = db.Column(db.String(35), unique=True, nullable=False)
    long_url = db.Column(db.String(2048), nullable=False)
    expire_date = db.Column(db.TIMESTAMP(timezone=False), nullable=False, default=datetime.now() + timedelta(days=90))

    def __init__(self, short_url, long_url, expire_date):
        self.short_url = short_url
        self.long_url = long_url
        self.expire_date = expire_date

    @classmethod
    def get_link(cls, id):
        return cls.query.get(id)

    @classmethod
    def create_link(cls, long_url, expire_date):
        base_url = 'http://test/'
        bts = os.urandom(4)
        short_url = b32encode(bts).decode('utf-8')
        link = Link.query.filter_by(short_url=base_url + short_url).first()

        if link and not link.is_link_expired():
            while Link.query.filter_by(short_url=base_url + short_url).first():
                bts = os.urandom(4)
                short_url = b32encode(bts).decode('utf-8')
        elif link:
            db.session.delete(link)

        new_link = cls(base_url + short_url, long_url, expire_date)
        db.session.add(new_link)
        db.session.commit()
        return new_link

    def delete_link(self):
        db.session.delete(self)

    @staticmethod
    def calculate_expire_date(days):
        return datetime.now() + timedelta(days=days)

    def is_link_expired(self):
        return datetime.now() > self.expire_date
