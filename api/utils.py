import json
import os
from functools import wraps

import jwt
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response


class ObjectResponse:
    def __init__(self, status, message, data):
        self.status = status
        self.message = message
        self.data = data

    def get_json(self):
        return {
            "status": self.status,
            "message": self.message,
            "data": self.data,
        }


class StatusResponse:
    STATUS_SUCCESS = "Success"
    STATUS_FAILED = "Failed"


class TokenJWT:
    def generate_token(payload):
        token = jwt.encode(
            payload, os.getenv("SECRET_KEY_JWT"), algorithm="HS256"
        )
        return token

    def decode_token(token):
        try:
            payload = jwt.decode(
                token, os.getenv("SECRET_KEY_JWT"), algorithms=["HS256"]
            )
            return payload
        except jwt.ExpiredSignatureError:
            return "Token has expired."
        except jwt.InvalidTokenError:
            return "Invalid token."


def is_valid_json(json_str):
    try:
        json.loads(json_str)
        return True
    except json.JSONDecodeError:
        return False


def try_except_wrapper(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except APIException as errors:
            return Response(
                errors.get_full_details(),
                status=errors.status_code,
            )
        except Exception as errors:
            return Response(
                {"errors": str(errors)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return wrapped
