from flask_restful import abort
from .models import Link


def get_link_or_404(id):
    link = Link.get_link(id)
    error_message = 'Link doesn\'t exist'
    if not link:
        abort(404, error=error_message)
    if link.is_link_expired():
        link.delete_link()
        abort(404, error=error_message)
    return link
