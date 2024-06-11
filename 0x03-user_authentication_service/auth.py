#!/usr/bin/env python3
"""auth"""
import bcrypt
from db import DB
from user import User


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
        if self._db.find_user_by(email=email):
            raise ValueError(f"User {email} already exists")
        else:
            hashed = _hash_password(password)
            return self._db.add_user(email=email, hashed_password=hashed.decode('utf-8'))
