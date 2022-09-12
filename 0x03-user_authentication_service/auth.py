#!/usr/bin/env python3
"""auth module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import bcrypt
from flask import request
import uuid
from typing import Union


def _hash_password(password: str) -> bytes:
    """returns bytes.
    """
    encoded = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(encoded, salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """return a User
        """
        try:
            find_user = self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            user = self._db.add_user(email, password)

        return user

    def valid_login(self, email: str, password: str) -> bool:
        """valid login
        """
        encoded = password.encode('utf-8')
        try:
            find_user = self._db.find_user_by(email=email)
            check_password = _hash_password(find_user.hashed_password)
            if bcrypt.checkpw(encoded, check_password):
                return True
        except NoResultFound:
            return False

        return False

    def create_session(self, email: str) -> str:
        """return the session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return

        new_UUID = _generate_uuid()
        user.session_id = new_UUID
        self._db._session.commit()

        return str(user.session_id)

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """"returns the corresponding User or None
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """updates the corresponding user’s session ID to None
        """
        try:
            user_id = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None
        user_id.session_id = None
        self._db._session.commit()

        return None

    def get_reset_password_token(self, email: str) -> str:
        """ If it exists, generate a UUID and
            update the user’s reset_token database field
            Return: the token
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()

        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Uses reset token to validate update of users password"""
        if reset_token is None or password is None:
            return None

        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        hashed_password = _hash_password(password)
        self._db.update_user(user.id,
                             hashed_password=hashed_password,
                             reset_token=None)


def _generate_uuid() -> str:
    """return a string representation of a new UUID
    """
    return str(uuid.uuid4())
