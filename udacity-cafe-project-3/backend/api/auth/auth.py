# import json
# from flask import request, _request_ctx_stack
from functools import wraps
# from jose import jwt
# from urllib.request import urlopen


AUTH0_DOMAIN = 'wildapps.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'fsnd-cafe'


# AuthError Exception
class AuthError(Exception):
    """
    AuthError Exception
    A standardized way to communicate auth failure modes
    """
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """
    TODO implement get_token_auth_header() method
        it should attempt to get the header from the request
            it should raise an AuthError if no header is present
        it should attempt to split bearer and the token
            it should raise an AuthError if the header is malformed
        return the token part of the header
    """
    raise Exception('Not Implemented')


def check_permissions(permission, payload):
    """
    TODO implement check_permissions(permission, payload) method
        it should raise an AuthError if permissions are not included in the payload
            !!NOTE check your RBAC settings in Auth0
        it should raise an AuthError if the requested permission string is not in the payload permissions array
        return true otherwise

    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload
    """
    raise Exception('Not Implemented')


def verify_decode_jwt(token):
    """
    TODO implement verify_decode_jwt(token) method
        it should be an Auth0 token with key id (kid)
        it should verify the token using Auth0 /.well-known/jwks.json
        it should decode the payload from the token
        it should validate the claims
        return the decoded payload

    @INPUTS
        token: a json web token (string)

    !!NOTE urlopen has a common certificate error described here:
    https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
    """
    raise Exception('Not Implemented')


def requires_auth(permission=''):
    """
    TODO implement @requires_auth(permission) decorator method
        it should use the get_token_auth_header method to get the token
        it should use the verify_decode_jwt method to decode the jwt
        it should use the check_permissions method validate claims and check the requested permission
        return the decorator which passes the decoded payload to the decorated method

    @INPUTS
        permission: string permission (i.e. 'post:drink')
    """
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
