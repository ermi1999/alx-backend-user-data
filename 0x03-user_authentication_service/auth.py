#!/usr/bin/env python3
"""auth"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """hash password"""
    password = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_password
