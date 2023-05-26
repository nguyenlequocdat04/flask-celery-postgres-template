from crypt import methods
from http import HTTPStatus
from flask import Blueprint, request

import pydash as py_
from sqlalchemy import text

import src.constants as Consts
import src.middlewares.http as Http
import src.functions as func

from src.extensions import redis_cached, session_scope

bp = Blueprint('index', __name__, url_prefix='/common')


@bp.route('debug')
@Http.make_cross_resp
def debug():
    1/0
    return ''


@bp.route('healthcheck')
@Http.make_cross_resp
def health_check():
    # redis
    redis_cached.ping()

    # db
    with session_scope() as session:
        result = session.execute(text("SELECT 1"))
        row = result.fetchone()
        print(row[0])  # Print the result value



    return {
        "code": HTTPStatus.OK,
        "msg": "success",
    }


@bp.route('reset')
@Http.make_cross_resp
def reset_mock_data():
    return {
        "code": HTTPStatus.OK,
        "msg": "success"
    }


@bp.route('celery', methods=['POST'])
@Http.make_cross_resp
def celery():
    from src.tasks import task_greeting
    payload = request.get_json()
    msg = py_.get(payload, "msg")

    task_greeting.delay(msg=msg)

    return {
        "code": HTTPStatus.OK,
        "msg": "success"
    }