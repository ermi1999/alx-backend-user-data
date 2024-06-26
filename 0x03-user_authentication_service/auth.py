#!/usr/bin/env python3
"""auth"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _generate_uuid() -> str:
    """generates uuid"""
    return str(uuid.uuid4())


def _hash_password(password: str) -> bytes:
    """hash password"""
    password = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register a new user"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed = _hash_password(password)
            return self._db.add_user(
                email=email, hashed_password=hashed.decode('utf-8'))

    def valid_login(self, email: str, password: str) -> bool:
        """valid login"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password.encode('utf-8'))
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """creates a session id for the email."""
        try:
            user = self._db.find_user_by(email=email)
            uid = _generate_uuid()
            self._db.update_user(user_id=user.id, session_id=uid)
            return uid
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """get user with a session id"""
        if not session_id:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """destroy session"""
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """gets a password reset token"""
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user_id=user.id, reset_token=reset_token)
            return reset_token
        except Exception:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """resets password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password).decode('utf-8')
            self._db.update_user(
                user.id, hashed_password=hashed_password,
                reset_token=None
                )
        except NoResultFound:
            raise ValueError
