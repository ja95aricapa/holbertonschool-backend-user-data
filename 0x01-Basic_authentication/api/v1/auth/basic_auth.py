#!/usr/bin/env python3
"""Class Basic_auth"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from api.v1.views.users import User
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """class Basic auth"""
    pass

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """returns the Base64 part of the Authorization header for a Basic"""
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        encoded = authorization_header.split(' ', 1)[1]

        return encoded

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                               str) -> str:
        """returns the decoded value of a Base64 string
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            encoded = base64_authorization_header.encode('utf-8')
            decoded64 = base64.b64decode(encoded)
            decoded = decoded64.decode('utf-8')
        except BaseException:
            return None

        return decoded

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                     str) -> (str, str):
        """returns the user email and password from the Base64 decoded
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        decoded = decoded_base64_authorization_header.split(":", 1)
        email = decoded[0]
        password = decoded[1]
        return email, password

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """returns the User instance based on his email and password.
        """
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        try:
            foundUsers = User.search({'email': user_email})
        except Exception:
            return None

        for user in foundUsers:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """retrieves the User instance for a request:
        """
        authorization = Auth()
        requests = authorization.authorization_header(request)
        extract = self.extract_base64_authorization_header(requests)
        decode = self.decode_base64_authorization_header(extract)
        extract_user = self.extract_user_credentials(decode)
        user_object = self.user_object_from_credentials(extract_user[0],
                                                        extract_user[1])
        return user_object
