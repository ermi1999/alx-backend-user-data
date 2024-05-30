#!/usr/bin/env python3
"""This module encrypts a password"""
import bcrypt


def hash_password(password: str) -> bytes:
    """this function hashes a password."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
