import os
import jwt
import hmac
import hashlib
import traceback

import pydash as py_

from libs.util_datetime import tzware_datetime


class SVC_Auth(object):
    def __init__(self, secret_key='', hash_salt='', algorithm='HS256'):
        self.secret_key = secret_key or os.getenv("JWT_SECRET")
        self.algorithm = algorithm or os.getenv("JWT_ALGORITHM")
        self.hash_salt = hash_salt or os.getenv("HMAC_SALT")

        if not self.secret_key or not self.hash_salt:
            raise Exception(f"SVC Auth require `JWT_SECRET` and `HMAC_SALT`")

    def hash(self, password: str) -> str:
        return hmac.new(
            self.hash_salt.encode('utf-8'),
            password.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def jwt_encode(self, payload) -> str:
        return jwt.encode(payload, self.secret_key, self.algorithm)

    def jwt_decode(self, token, options={}) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, [self.algorithm], options=options)
            return payload
        except:
            traceback.print_exc()
            return None


if __name__ == "__main__":
    import datetime as dt
    svc_auth = SVC_Auth('1234', '123123')

    value = svc_auth.hash('password')
    print(f"HASH: {value} - {type(value)}")

    now = int(dt.datetime.now().timestamp())

    payload_jwt = {
        "iss": 'hlo',
        "exp": now,
        "iat": now,
        "uid": str("123456"),
        "rst": False
    }

    token = svc_auth.jwt_encode(payload_jwt)
    print(f"Token encode: {token} - {type(token)}")
    print(f"Token decode: {svc_auth.jwt_decode(token)}")
