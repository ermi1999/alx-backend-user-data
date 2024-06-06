#!/usr/bin/env python3
"""Basic auth
"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """Baic auth
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extracts authorization header.
        """
        if not authorization_header or type(authorization_header) is not str:
            return None

        basic = authorization_header[:6]
        if basic != "Basic ":
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decode base64
        """
        if not base64_authorization_header or type(
                base64_authorization_header) is not str:
            return None
        try:
            result = base64.b64decode(
                    base64_authorization_header, validate=True)
            return result.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """extract credentials."""
        if (not decoded_base64_authorization_header or
                type(decoded_base64_authorization_header)is not str or
                ":" not in decoded_base64_authorization_header):
            return (None, None)
        header = decoded_base64_authorization_header.split(':', 1)
        return (header[0], header[1])

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """User object from credentials"""
        if type(user_email) != str or type(user_pwd) != str:
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        if len(users) <= 0:
            return None
        if users[0].is_valid_password(user_pwd):
            return users[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user."""
        user_credentials = self.extract_user_credentials(
            self.decode_base64_authorization_header(
                self.extract_base64_authorization_header(
                    self.authorization_header(request))))
        return self.user_object_from_credentials(
                user_credentials[0], user_credentials[1])
