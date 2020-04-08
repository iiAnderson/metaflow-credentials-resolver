
class LambdaException(Exception):

    def __init__(self, msg, code):
        super().__init__(msg)

        self.http_code = code
