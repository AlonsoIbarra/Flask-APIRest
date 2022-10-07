from jwt import encode, decode, exceptions
from os import getenv
from datetime import datetime, timedelta
from flask import request, jsonify


def expiration_date():
    today = datetime.today()
    expiration_date = today + timedelta(
        days=int(getenv("EXPIRATION_DAYS"))
    )
    return expiration_date


def write_token(data: dict):
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
    if 'Authorization' not in request.headers:
        response = jsonify({
            "success": False,
            "error": "Authentication needed"
        })
        response.status_code = 401
        return response
    token = request.headers['Authorization'].split(' ')[1]
    return validate_token(token)
