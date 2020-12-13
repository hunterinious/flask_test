from flask import request, jsonify, redirect
from marshmallow import ValidationError
from flask_restful import Resource, abort
from .models import Link
from .schemas import LinkSchema, LinkCreateSchema


class LinkAPI(Resource):
    def post(self):
        json_data = request.get_json()
        days = json_data.get('days')
        long_url = json_data.get('long_url')

        try:
            LinkCreateSchema().load(json_data)
        except ValidationError as error:
            return error.messages, 400

        expire_date = Link.calculate_expire_date(days)
        link = Link.create_link(long_url, expire_date)

        return jsonify(LinkSchema().dump(link), 200)


class LinkRedirectAPI(Resource):
    def get(self, id):
        link = Link.get_link(id)
        error_message = 'Link doesn\'t exist'
        if not link:
            abort(404, error=error_message)
        if link.is_link_expired():
            link.delete_link()
            abort(404, error=error_message)
        return redirect(link.long_url, code=302)
