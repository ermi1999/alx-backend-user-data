#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import User
from typing import TypeVar

from user import Base


class DB:
    """DB class
    """

    def __init__(self) -> None:
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
        """creates a user"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """find user"""
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except Exception:
            raise

    def update_user(self, user_id: int, **kwargs) -> None:
        """updates a user"""
        user = self.find_user_by(id=user_id)
        columns = User.__table__.columns.keys()
        for key, value in kwargs.items():
            if key not in columns:
                raise ValueError
            setattr(user, key, value)
        self._session.add(user)
        self._session.commit()
