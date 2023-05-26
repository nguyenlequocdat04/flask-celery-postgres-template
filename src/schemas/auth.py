from flask_restx import Namespace, fields

from .api import BaseMeta


class Meta(BaseMeta):
    api = Namespace('Authentication', description='')

    response = api.model('Response', {
        'msg': fields.String(default="unknown"),
        'code': fields.Integer(default=0),
        'data': fields.Raw()
    })

    in_login = api.model('InputLogin', {
        'custom_id': fields.String(description='Custom id'),
    })
