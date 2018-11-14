from flask import request
from library.security.TokenHandler import validate_token


def authorize(funct):
    def wrapper(*args):
        token = request.headers["Token"]
        validate_token(token)
        return funct(*args)
    return wrapper

