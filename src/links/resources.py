from flask import request, jsonify, redirect
from marshmallow import ValidationError
from flask_restful import Resource
from .models import Link
from .schemas import LinkSchema, LinkCreateSchema
from .shortcuts import get_link_or_404


class CreateLinkAPI(Resource):
    def post(self):
        json_data = request.get_json()
        days = json_data.get('days')
        long_url = json_data.get('long_url')

        try:
            LinkCreateSchema().load(json_data)
        except ValidationError as error:
            return error.messages, 400

        expire_date = Link.calculate_expire_date(days) if days else None
        link = Link.create_link(long_url, expire_date)

        return jsonify(LinkSchema().dump(link))


class RetrieveLinkAPI(Resource):
    def get(self, id):
        link = get_link_or_404(id)
        return jsonify(LinkSchema().dump(link))


class LinkRedirectAPI(Resource):
    def get(self, id):
        link = get_link_or_404(id)
        return redirect(link.long_url, code=302)
