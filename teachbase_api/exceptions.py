class TeachbaseApiException(Exception):
    pass


class AuthError(TeachbaseApiException):
    pass


class BadRequest(TeachbaseApiException):
    pass
