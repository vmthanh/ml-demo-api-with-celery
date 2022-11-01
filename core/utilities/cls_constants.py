class APIReplyBase:
    TEXT_BY_CODE = {}

    @classmethod
    def text(cls, code):
        return cls.TEXT_BY_CODE.get(code, "")


class APIReply(APIReplyBase):

    SUCCESS = 0

    ERROR_SERVER = 101

    TEXT_BY_CODE = {
        SUCCESS: "Successful",
        ERROR_SERVER: "Server errors with caught exceptions",
    }
