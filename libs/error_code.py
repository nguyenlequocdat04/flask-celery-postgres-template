
class CodeMsg(object):
    def __init__(self, msg="success", code=200, data={}) -> None:
        self.msg = msg
        self.code = code
        self.data = data

    def to_json(self, data={}, msg=""):
        return {
            "msg": msg or self.msg,
            "code": self.code,
            "data": data,
        }


class RespMsg(object):
    SUCCESS = CodeMsg()
    INVALID = CodeMsg("invalid", 400)
    FAIL = CodeMsg("fail", 400)

    NOT_FOUND = CodeMsg("not_found", 404)
    USER_NOT_FOUND = CodeMsg("user_not_found", 404)
    UNAUTHORIZED = CodeMsg("unauthorized", 401)
    PAYMENT_REQUIRE = CodeMsg("payment_require", 402)
