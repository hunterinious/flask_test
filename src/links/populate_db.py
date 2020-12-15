from src.flask_test.db import db
from .models import Link
from datetime import datetime


def create_links_from_json(json_links):
    links = []
    for link in json_links:
        year, month, day, hour, minutes = link['expire_date'].split('-')
        expire_date = datetime(int(year), int(month), int(day), int(hour), int(minutes))
        link = Link(long_url=link['long_url'], short_url=link['short_url'], expire_date=expire_date)
        links.append(link)
        db.session.add(link)

    db.session.commit()
    return links


