class ApiException(Exception):
    def __init__(self, msg="success", code=200, data={}) -> None:
        self.msg = msg
        self.code = code
        self.data = data

    def to_json(self, data=None, msg=""):
        if data is not None:
            return {
                "msg": msg or self.msg,
                "code": self.code,
                "data": data,
            }

        return {
            "msg": msg or self.msg,
            "code": self.code,
        }


class RespMsg(object):
    SUCCESS = ApiException()
    COMMING_SOON = ApiException("comming_soon", 500)

    INVALID = ApiException("invalid", 400)
    FAIL = ApiException("fail", 400)

    NOT_FOUND = ApiException("not_found", 404)
    USER_NOT_FOUND = ApiException("user_not_found", 404)
    UNAUTHORIZED = ApiException("unauthorized", 401)
    PAYMENT_REQUIRE = ApiException("payment_require", 402)

    RECEIPT_ALREADY_USED = ApiException("receipt_already_used", 400)
