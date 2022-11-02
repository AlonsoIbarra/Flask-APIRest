from jwt import encode, decode, exceptions
from os import getenv
from datetime import datetime, timedelta
from flask import request, jsonify


def expiration_date():
    """
    Return a date in the future as expiraton days says.
    """
    today = datetime.today()
    expiration_date = today + timedelta(
        days=int(getenv("EXPIRATION_DAYS"))
    )
    return expiration_date


def write_token(data: dict):
    """
    Write a token in jwt database library to check api access.
    Params:
        data dict Any Python dictionary to encript.
    """
    token = encode(
        payload={
            **data,
            "exp": expiration_date()
        },
        key=getenv("SECRET"),
        algorithm="HS256"
    )
    return token


def validate_token(token, output=False):
    """
    Validates a given token in jwt database library.
    Params:
        token  string  A valid string token.
        output bool    If the validation result should be return.
    """
    try:
        if output:
            return decode(
                token,
                key=getenv("SECRET"),
                algorithms=["HS256"]
            )
        decode(
            token,
            key=getenv("SECRET"),
            algorithms=["HS256"]
        )
    except exceptions.DecodeError:
        response = jsonify({
            "success": False,
            "error": "Invalid Token"
        })
        response.status_code = 401
        return response
    except exceptions.ExpiredSignatureError:
        response = jsonify({
            "success": False,
            "error": "Token Expired"
        })
        response.status_code = 401
        return response


def verify_token_middleware():
    """
    Function to validate a Barier token from request header.
    """
    if 'Authorization' not in request.headers:
        response = jsonify({
            "success": False,
            "error": "Authentication needed"
        })
        response.status_code = 401
        return response
    token = request.headers['Authorization'].split(' ')[1]
    return validate_token(token)
