from src.flask_test.db import db
from .models import Link
from datetime import datetime


def create_links_from_json(json_links):
    links = []
    for link in json_links:
        expire_date = datetime.strptime(link['expire_date'], "%Y-%m-%d-%H-%M")
        link = Link(long_url=link['long_url'], short_url=link['short_url'],
                    expire_date=expire_date, is_expired=bool(link['is_expired']))
        links.append(link)
        db.session.add(link)

    db.session.commit()
    return links


