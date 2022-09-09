#!/usr/bin/env python3
"""Module of class auth"""
from flask import request, make_response
from typing import List, TypeVar
from os import getenv


class Auth:
    """class Auth"""

    def __init__(self):
        """method constructor"""
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """public method require_auth

        Returns:
            False or True
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != "/":
            path += "/"
        if excluded_paths[-1] != "/":
            excluded_paths += "/"
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """public method authorization_header

        Returns:
            None
        """
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar("User"):
        """public method current_user

        Returns:
            None
        """
        return None

    def session_cookie(self, request=None) -> str:
        """public method session_cookie"""
        if request is None:
            return None
        name_cookie = getenv("SESSION_NAME")
        return request.cookies.get(name_cookie)
