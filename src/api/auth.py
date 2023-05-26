import traceback
import pydash as py_

from flask import request
from flask_restx import Resource, marshal

import src.constants as Consts
import src.decorators as Decorators
import src.controllers as Ctrls
import src.functions as Funcs

from libs.util_datetime import tzware_timestamp

from src.config import DefaultConfig as Conf
from src.schemas import AuthMeta as MetaSchema
from libs.exceptions import ApiException, RespMsg

api = MetaSchema.api


@api.route('/login')
@api.doc(responses=MetaSchema.RESPONSE_CODE)
class Login(Resource):
    @api.expect(MetaSchema.in_login)
    @api.marshal_with(MetaSchema.response)
    def post(self):
        """
        """
        try:
            obj = marshal(request.get_json(), MetaSchema.in_login)

            return RespMsg.SUCCESS.to_json()
        except ApiException as e:
            traceback.print_exc()
            return e.to_json()
