from src.flask_test.db import db
from datetime import datetime, timedelta
from base64 import b32encode
import os


class Link(db.Model):
    MAXIMAL_ALLOWED_URL_LENGTH = 2048
    NUMBER_OF_RANDOM_BYTES_FOR_SHORT_URL = 4

    __tablename__ = 'links'
    id = db.Column(db.BigInteger, primary_key=True)
    short_url = db.Column(db.String(35), unique=True, nullable=False)
    long_url = db.Column(db.String(MAXIMAL_ALLOWED_URL_LENGTH), nullable=False)
    expire_date = db.Column(db.TIMESTAMP(timezone=False), nullable=False,
                            default=datetime.now() + timedelta(days=int(os.environ.get('DEFAULT_STORAGE_DAYS'))))
    is_expired = db.Column(db.Boolean, nullable=False, default=False)

    __table_args__ = (
        db.Index('links_short_url_not_expired_index', short_url,
                 postgresql_where=(~is_expired)),
    )

    @property
    def expired(self):
        return self.is_expired

    @expired.setter
    def expired(self, expired):
        self.is_expired = expired
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_link(cls, id):
        return cls.query.get(id)

    @classmethod
    def create_link(cls, long_url, expire_date):
        bts = os.urandom(cls.NUMBER_OF_RANDOM_BYTES_FOR_SHORT_URL)
        short_url = b32encode(bts).decode('utf-8')
        link = Link.query.filter_by(short_url=short_url).first()
        link_expired = link.is_link_expired() if link else False

        if link and not link_expired:
            while Link.query.filter_by(short_url=short_url).first():
                bts = os.urandom(4)
                short_url = b32encode(bts).decode('utf-8')
        elif link_expired:
            link.expired = True

        new_link = cls(short_url=short_url, long_url=long_url, expire_date=expire_date)
        db.session.add(new_link)
        db.session.commit()
        return new_link

    @staticmethod
    def calculate_expire_date(days):
        return datetime.now() + timedelta(days=days)

    def is_link_expired(self):
        return datetime.now() > self.expire_date
