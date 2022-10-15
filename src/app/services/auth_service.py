import base64
import os
import tornado

from functools import wraps
from typing import List

from unittest import expectedFailure

from app import BASIC_AUTH_PASSWORD, BASIC_AUTH_USERNAME

from tornado.web import RequestHandler


class BasicAuthService:
    def __init__(self, request: RequestHandler) -> None:
        self.request = request
        self.expected_username = BASIC_AUTH_USERNAME
        self.expected_password = BASIC_AUTH_PASSWORD

    def send_auth_challenge(self):
        hdr = "Basic realm=Restricted"
        self.request.set_status(401)
        self.request.set_header("www-authenticate", hdr)
        self.request.write({"message": "Invalid credentials. Please check your Authorization headers and try again."})
        self.request.finish()
        return False

    def authenticate_user(self) -> bool:
        print("foo")
        auth_header = self.request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Basic "):
            raise self.SendChallenge()

        auth_data = auth_header.split(None, 1)[-1]
        auth_data = base64.b64decode(auth_data).decode("ascii")
        username, password = auth_data.split(":", 1)

        return self.validate_credentials(username, password)

    def validate_credentials(self, username: str, password: str) -> bool:
        return username == self.expected_username and password == self.expected_password


def auth_required(handler_class: RequestHandler):
    """Decorator that protect methods with HTTP authentication."""

    def decorator(func):
        #### STILL NOT WORKING - HANGING AFTER NEXT LINE
        print("qqq")

        @tornado.gen.coroutine
        @wraps(func)
        def wrapper(*args, **kwargs):
            print("wwww")
            service = BasicAuthService(request=handler_class)

            if service.authenticate_user():
                print("aaaa")
                result = yield func(*args, **kwargs)
            else:
                print("bbbb")
                result = service.send_auth_challenge()

            print(result)

        return wrapper

    return decorator
