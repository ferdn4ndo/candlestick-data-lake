import base64
import os

from unittest import expectedFailure

from app import BASIC_AUTH_PASSWORD, BASIC_AUTH_USERNAME


def validate_credentials(username: str, password: str) -> bool:
    expected_username = BASIC_AUTH_USERNAME
    expected_password = BASIC_AUTH_PASSWORD
    
    return username == expected_username and password == expected_password


def require_basic_auth(handler_class):
    # Should return the new _execute function, one which enforces authentication and only calls the inner handler's
    # _execute() if it's present.
    def wrap_execute(handler_execute):
        # I've pulled this out just for clarity, but you could stick it in _execute if you wanted. It returns True if
        # credentials were provided and are valid.
        def require_basic_auth(handler, kwargs):
            auth_header = handler.request.headers.get('Authorization')
            if auth_header is None or not auth_header.startswith('Basic '):
                # If the browser didn't send us authorization headers, send back a response letting it know that we'd
                # like a username and password (the "Basic" authentication method). Without this, even if you visit
                # put a username and password in the URL, the browser won't send it. The "realm" option in the header
                # is the name that appears in the dialog that pops up in your browser.
                handler.set_status(401)
                handler.set_header('WWW-Authenticate', 'Basic realm=Restricted')
                handler._transforms = []
                handler.finish()
                
                return False
            # The information that the browser sends is base64-encoded, and in the format "username:password".Keep in
            # mind that either username or password could still be unset.
            auth_decoded = base64.decodestring(auth_header[6:])
            username, password = auth_decoded.split(':', 2)
            
            return validate_credentials(username=username, password=password)

        # Since we're going to attach this to a RequestHandler class, the first argument will wind up being a reference
        # to an instance of that class.
        def _execute(self, transforms, *args, **kwargs):
            if not require_basic_auth(self, kwargs):
                return False
            
            return handler_execute(self, transforms, *args, **kwargs)

        return _execute

    handler_class._execute = wrap_execute(handler_class._execute)
    
    return handler_class
