from flask import request
from library.security.TokenHandler import validate_token


def authorize(funct):
    """
    Decorator design for rest api. It validates the headers for valid token
    :param funct: the function that is decorated
    :return: wrapper function
    """
    def wrapper(*args):
        """
        Wrapper function that validated token before implementation validataion
        :param args: arguments of the function that is being decorated
        :return:
        """
        token = request.headers["Token"]
        validate_token(token)
        return funct(*args)
    return wrapper

