import jwt
import calendar
import time
import datetime
from flask import abort
TEMP_KEY = 'SECRET_KEY'
ALGO = 'HS256'



def time_now():
    return datetime.datetime.utcnow()


def epoch(time_object):
    return calendar.timegm(time.strptime(time_object.strftime("%a %b %d %H:%M:%S %Y")))


def expired_time(time_object):
    return time_object + datetime.timedelta(hours=24)


# https://pyjwt.readthedocs.io/en/latest/installation.html
def create_token():
    now = time_now()
    exp = expired_time(now)

    return jwt.encode({"application": "SFO Spock Update Service", "version": "1.0", "iat": now,
                       "exp": exp}, TEMP_KEY, algorithm=ALGO).decode("utf-8", "strict")


def validate_token(token):
    try:
        jwt.decode(str.encode(token, encoding="utf-8"), TEMP_KEY, leeway=30, algorithms=ALGO)
    except jwt.ExpiredSignatureError:
        abort(400, {'message': 'Invalid token. Please reauthorize'})
