#!/usr/bin/env python3
"""Module of class auth"""
from api.v1.auth.auth import Auth
import uuid
from models.base import Base
from models.user import User


class SessionAuth(Auth):
    """class SessionAuth"""

    user_id_by_session_id = dict()

    def create_session(self, user_id: str = None) -> str:
        """instance method create_session"""
        if user_id is None:
            return None
        if type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """instance method user_id_for_session_id"""
        if session_id is None:
            return None
        if type(session_id) is not str:
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        self.user_id_by_session_id[session_id] = user_id

        return user_id

    def current_user(self, request=None):
        """instance method current_user"""
        session_cookie = self.session_cookie(request)
        session_id = self.user_id_for_session_id(str(session_cookie))

        return User.get(session_id)

    def destroy_session(self, request=None):
        """instance method destroy_session"""
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False

        user_id = self.user_id_for_session_id(session_cookie)
        if not user_id:
            return False

        del self.user_id_by_session_id[session_cookie]

        return True
