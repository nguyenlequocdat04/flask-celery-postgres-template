import hashlib
import json
from datetime import datetime, date, timedelta

import redis
from flask import request
from src.extensions import redis_cached, session_scope

def json_decode_hook(obj):
    if '__datetime__' in obj:
        return datetime.strptime(obj['as_str'], "%Y%m%dT%H:%M:%S.%f")
    if b'__datetime__' in obj:
        return datetime.strptime(obj[b'as_str'], "%Y%m%dT%H:%M:%S.%f")
    return obj


def json_encode_hook(obj):
    if isinstance(obj, datetime):
        obj = {
            '__datetime__': True,
            'as_str': obj.strftime("%Y%m%dT%H:%M:%S.%f")
        }
    if isinstance(obj, date):
        dt = datetime.combine(obj.today(), datetime.min.time())
        obj = {
            '__datetime__': True,
            'as_str': dt.strftime("%Y%m%dT%H:%M:%S.%f")
        }
    return obj


def json_encode_response(obj):
    if isinstance(obj, datetime):
        return obj.timestamp()
    if isinstance(obj, date):
        return datetime.combine(obj.today(), datetime.min.time()).timestamp()
    return obj


def sha1(data):
    json_data = json.dumps(data, default=json_encode_hook)
    return hashlib.sha1(json_data.encode('utf-8')).hexdigest()


# def check_redis_connection():
#     try:
#         redis_cached.ping()
#     except (redis.exceptions.ConnectionError, redis.exceptions.BusyLoadingError):
#         return False
#     return True


# def check_db_connection():
#     try:
#         redis_cached.ping()
#     except (redis.exceptions.ConnectionError, redis.exceptions.BusyLoadingError):
#         return False
#     return True

