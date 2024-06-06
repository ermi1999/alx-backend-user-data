#!/usr/bin/env python3
"""
Auth
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """A class for handling authentication.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """to be documented
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != '*':
            if path[-1] != "/":
                path = path + "/"
            if path in excluded_paths:
                return False
            return True
        for excluded_path in excluded_paths:
            if path[:-1] == excluded_path[:len(path) - 2]:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization header
        """
        if request is not None:
            return request.headers.get("Authorization")
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current user
        """
        return None
