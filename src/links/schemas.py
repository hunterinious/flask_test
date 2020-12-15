from src.flask_test.marshmallow import ma
from marshmallow import Schema, fields, ValidationError
from .models import Link
import re
import os


def validate_days(days):
    if days > 365:
        raise ValidationError("Expire can\'t be more than 1 year")
    if days < 1:
        raise ValidationError("Expire can\'t be less than 1 day")


def validate_long_url(url):
    regex = re.compile(
        r'^((?:http|ftp)s?://)?'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?))'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if not bool(re.match(regex, url)):
        raise ValidationError('Please, give a valid url')
    if len(url) > 2048:
        raise ValidationError('Long url allows no more than 2048 characters')


class LinkCreateSchema(Schema):
    long_url = fields.Str(required=True, validate=validate_long_url)
    days = fields.Int(required=False, validate=validate_days)


class LinkSchema(ma.Schema):
    short_url = fields.Method('get_short_url')

    class Meta:
        fields = ('id', 'short_url', 'long_url')

    def get_short_url(self, obj):
        return os.environ.get('BASE_URL') + obj.short_url