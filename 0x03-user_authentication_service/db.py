#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session, SessionTransaction
from typing import Any
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base
from user import User


class DB:
    """DB class for Object Reational Mappin
    """

    def __init__(self):
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """The method should save the user to the database

        arguments:
            email(string)
            hashed_password(string)

        returns:
            returns a User object
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """returns the first row found in the users
        table as filtered by the method’s input arguments.
        """
        if not kwargs:
            raise InvalidRequestError
        column_name = User.__table__.columns.keys()

        for key in kwargs.keys():
            if key not in column_name:
                raise InvalidRequestError

        return self._session.query(User).filter_by(**kwargs).one()

    def update_user(self, user_id: int, **kwargs) -> None:
        """locate the user to update
        """
        column_name = User.__table__.columns.keys()

        for key in kwargs.keys():
            if key not in column_name:
                raise ValueError

        locate_user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            locate_user.key = value

        self._session.commit()
