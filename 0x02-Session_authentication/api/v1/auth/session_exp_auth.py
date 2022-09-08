#!/usr/bin/env python3
"""
Module of  expiration date to a Session ID.
"""
from datetime import datetime, timedelta
from os import getenv

from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    class SessionAuth
    """

    def __init__(self):
        """
        constructor method
        """
        try:
            self.session_duration = int(getenv("SESSION_DURATION", 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        create session method
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        SessionExpAuth.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now(),
        }

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        user id for session id method
        """
        if session_id is None:
            return None
        session_dictionary = SessionExpAuth.user_id_by_session_id.get(
            session_id,
            None
            )
        if session_dictionary is None:
            return None
        if self.session_duration <= 0:
            return session_dictionary.get("user_id")
        if "created_at" not in session_dictionary:
            return None
        created_at = session_dictionary.get("created_at")
        session_length = timedelta(seconds=self.session_duration)
        expiry_time = created_at + session_length

        if expiry_time < datetime.now():
            return None

        return session_dictionary.get("user_id")
